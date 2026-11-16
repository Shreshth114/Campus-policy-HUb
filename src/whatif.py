"""Transient deterministic scenarios over current quote-validated personal rules."""
from decimal import Decimal, localcontext, ROUND_CEILING, ROUND_FLOOR
import asyncio
import secrets
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from src import intelligence, personal, institutions

router=APIRouter()
LIMIT=Decimal('1000000000000')


def numeric(value):
    if isinstance(value,bool) or len(str(value))>64:raise ValueError('Invalid numeric value')
    result=Decimal(str(value))
    if not result.is_finite() or abs(result)>LIMIT or result<0 or result.as_tuple().exponent < -24:
        raise ValueError('Values must be finite, nonnegative, at most 1e12 and have at most 24 decimal places')
    return result


class Fact(BaseModel):
    model_config=ConfigDict(extra='forbid')
    subject:StrictStr=Field(min_length=1,max_length=100)
    value:StrictStr
    unit:StrictStr=Field(max_length=50)


class Counts(BaseModel):
    model_config=ConfigDict(extra='forbid')
    done:int=Field(strict=True,ge=0,le=1000000000)
    total:int=Field(strict=True,gt=0,le=1000000000)
    remaining:int|None=Field(default=None,strict=True,ge=0,le=1000000000)


class Scenario(BaseModel):
    model_config=ConfigDict(extra='forbid')
    facts:list[Fact]=Field(max_length=40)
    rule_ids:list[StrictStr]=Field(default_factory=list,max_length=100)
    counts:dict[str,Counts]=Field(default_factory=dict,max_length=40)
    confirmed:StrictBool=False
    applicability_confirmed:StrictBool=False


def count_path(operator,threshold,done,total,remaining=None):
    """Integer arithmetic uses high precision Decimal, with no institutional rounding assumption."""
    with localcontext() as context:
        context.prec=80
        t=numeric(threshold);d=numeric(done);n=numeric(total)
        if not n or d>n or d!=d.to_integral_value() or n!=n.to_integral_value():raise ValueError('Counts require integers with 0 <= done <= total and total > 0')
        compare=intelligence.OPERATORS[operator]
        deficit=t*n-100*d;gain=100-t
        result={'current_percent':str(100*d/n),'additional_completed':None,'reason':None}
        if compare(100*d,t*n):result['additional_completed']=0
        elif operator in ('>=','>') and gain>0:
            x=(deficit/gain).to_integral_value(rounding=ROUND_CEILING if operator=='>=' else ROUND_FLOOR)
            result['additional_completed']=max(0,int(x)+(operator=='>'))
        elif operator=='==' and gain>0:
            x=deficit/gain
            if x>=0 and x==x.to_integral_value():result['additional_completed']=int(x)
        if result['additional_completed'] is None:result['reason']='Cannot meet this operator and threshold by additional fully completed items alone.'
        if remaining is not None:
            r=numeric(remaining)
            if r!=r.to_integral_value():raise ValueError('Remaining must be an integer')
            needed=t*(n+r)/100-d
            if operator in ('>=','>'):
                completed=max(0,int(needed.to_integral_value(rounding=ROUND_CEILING if operator=='>=' else ROUND_FLOOR))+(operator=='>'))
                missed=int(r)-completed if completed<=r else None
            elif operator in ('<=','<'):
                missed=int(r) if compare(100*d,t*(n+r)) else None
            elif operator=='==':missed=int(r-needed) if needed==needed.to_integral_value() and 0<=needed<=r else None
            else:
                missed=int(r) if compare(100*d,t*(n+r)) else int(r)-1 if r else None
            result.update(reachable=missed is not None,max_remaining_missed=missed,all_completed_meets=compare(100*(d+r),t*(n+r)),all_completed_percent=str(100*(d+r)/(n+r)))
        return result


def gap(rule,value):
    threshold=Decimal(str(rule['value']));current=Decimal(value);operator=rule['operator']
    if operator=='==':return {'amount':None,'direction':'equal','boundary':str(threshold),'strict':False}
    if operator=='!=':return {'amount':None,'direction':'different','boundary':str(threshold),'strict':False}
    return {'amount':str(abs(threshold-current)),'direction':'increase' if operator in ('>=','>') else 'decrease','boundary':str(threshold),'strict':operator in ('>','<')}


def simulate(body):
    rules=intelligence.list_rules();selected=set(body.rule_ids)
    available={r['rule_id'] for r in rules}
    if not selected.issubset(available):raise ValueError('Analysis rules changed or are unavailable in this workspace. Run analysis again.')
    rules=[r for r in rules if r['rule_id'] in selected]
    facts=[f.model_dump() for f in body.facts]
    for fact in facts:
        value=numeric(fact['value'])
        if intelligence.unit(fact['unit'])=='%' and value>100:raise ValueError('Percentage values must be between 0 and 100')
    for subject,counts in body.counts.items():
        if counts.done>counts.total:raise ValueError('Done must not exceed total')
        matches=[f for f in facts if f['subject']==subject]
        if len(matches)==1 and intelligence.unit(matches[0]['unit'])=='%':
            with localcontext() as context:
                context.prec=80;matches[0]['value']=str(Decimal(100)*counts.done/counts.total)
    conflicted={c['subject'] for c in intelligence.conflicts_from_rules(intelligence.list_rules())}
    computed=intelligence.evaluate(rules,facts if body.confirmed else [],body.applicability_confirmed,conflicted)
    for condition in computed['conditions']:
        rule=condition['rule'];condition.update(gap=None,counts=None)
        usable=body.confirmed and body.applicability_confirmed and condition['status']!='insufficient evidence' and rule['subject'] not in conflicted
        if usable and condition['status']=='not satisfied':condition['gap']=gap(rule,condition['your_value'])
        if usable and rule['unit']=='%' and rule['subject'] in body.counts:
            counts=body.counts[rule['subject']];condition['counts']=count_path(rule['operator'],rule['value'],counts.done,counts.total,counts.remaining)
    # Only reorder unmet conditions among positions sharing the same unit.
    for unit in dict.fromkeys(c['rule']['unit'] for c in computed['conditions']):
        positions=[i for i,c in enumerate(computed['conditions']) if c['rule']['unit']==unit and c['gap'] and c['gap']['amount'] is not None]
        ordered=sorted((computed['conditions'][i] for i in positions),key=lambda c:Decimal(c['gap']['amount']))
        for i,c in zip(positions,ordered):computed['conditions'][i]=c
    computed.update(conflicted=any(r['subject'] in conflicted for r in rules),trust_notice=personal.TRUST_NOTICE,scenario_only=True,arithmetic_notice='ARITHMETIC ON THE STATED THRESHOLD ONLY. Counting rules, cut-off dates, condonation, exceptions and rounding practices are not modelled.')
    if computed['conflicted']:
        computed['verdict']=None
        for condition in computed['conditions']:condition['gap']=None;condition['counts']=None
    return computed


@router.post('/api/personal/{workspace}/whatif')
async def whatif(workspace:str,body:Scenario,x_workspace_id:str|None=Header(default=None)):
    if not x_workspace_id or not secrets.compare_digest(workspace,x_workspace_id):raise HTTPException(404,'Personal workspace unavailable')
    try:ctx=personal.resolve(workspace)
    except ValueError:raise HTTPException(404,'Personal workspace unavailable')
    try:
        with institutions.scope(ctx):return await asyncio.to_thread(simulate,body)
    except (ValueError,ArithmeticError) as error:raise HTTPException(422,str(error))
