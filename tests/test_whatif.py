import hashlib,json,random
from decimal import Decimal
from pathlib import Path
from unittest.mock import Mock
import pytest
from src import whatif,intelligence,personal,institutions
from src.persistence import write_json
from tests.test_personal import client,create,uploaded

@pytest.mark.parametrize('op,value,status', [('>=','75','satisfied'),('>','75','not satisfied'),('<=','75','satisfied'),('<','75','not satisfied'),('==','75','satisfied')])
def test_operator_boundaries(op,value,status):
    rule={'subject':'x','operator':op,'value':'75','unit':'%','exceptions':[]}
    assert intelligence.evaluate([rule],[{'subject':'x','value':value,'unit':'%'}],True)['conditions'][0]['status']==status
    if op=='==':assert whatif.gap(rule,'70')['amount'] is None


def test_counts_boundary_and_remaining():
    assert whatif.count_path('>=',75,60,90)['additional_completed']==30
    assert whatif.count_path('>',75,60,90)['additional_completed']==31
    assert whatif.count_path('>=',100,60,90)['additional_completed'] is None
    assert whatif.count_path('>=',100,90,90)['additional_completed']==0
    assert whatif.count_path('>',100,90,90)['additional_completed'] is None
    assert whatif.count_path('>=',75,60,90,30)['max_remaining_missed']==0
    assert whatif.count_path('>=',75,60,90,29)['reachable'] is False
    assert whatif.count_path('>=',75,60,90,50)['max_remaining_missed']==5
    assert whatif.count_path('>',75,90,90,2)['max_remaining_missed']==2
    assert whatif.count_path('<=',75,60,90,20)['max_remaining_missed']==20
    assert whatif.count_path('==',75,60,90,30)['max_remaining_missed']==0


def test_300_random_count_cases_against_independent_integer_loop():
    rng=random.Random(418)
    for _ in range(300):
        n=rng.randint(1,50);d=rng.randint(0,n);t=rng.randint(0,100);remaining=rng.randint(0,30);op=rng.choice(['>=','>','<=','<','=='])
        compare=intelligence.OPERATORS[op]
        # Bound 100*n+1 covers any finite first success for integer percentages <100.
        expected=next((x for x in range(100*n+2) if compare(100*(d+x),t*(n+x))),None)
        actual=whatif.count_path(op,t,d,n,remaining)
        assert actual['additional_completed']==expected,(op,t,d,n)
        misses=[m for m in range(remaining+1) if compare(100*(d+remaining-m),t*(n+remaining))]
        assert actual['max_remaining_missed']==(max(misses) if misses else None)

@pytest.mark.parametrize('value',['NaN','Infinity','-1','1000000000001','1e-25'])
def test_invalid_numbers(value):
    with pytest.raises(ValueError):whatif.numeric(value)

@pytest.mark.parametrize('done,total',[(1,0),(-1,20),(21,20)])
def test_invalid_counts(done,total):
    with pytest.raises((ValueError,ArithmeticError)):whatif.count_path('>=',75,done,total)


def seed(client,headers,wid):
    source=uploaded(client,headers)
    ctx=personal.resolve(wid)
    with institutions.scope(ctx):
        entry=intelligence.document_entry(source['doc_id']);chunk=intelligence.chunks_for(entry)[0]
        rule=intelligence.validate_rule({'subject':'attendance','operator':'>=','value':75,'unit':'%','verbatim_quote':'Minimum attendance is at least 75 percent.','exceptions':[]},chunk)
        assert rule
        write_json(ctx.processed/'rules.json',{intelligence._key(entry):{'rules':[rule]}})
    return rule


def request(rule,**changes):
    return dict(facts=[{'subject':'attendance','value':'70','unit':'%'}],rule_ids=[rule['rule_id']],confirmed=True,applicability_confirmed=True,**changes)


def test_scoped_endpoint_zero_provider_calls_no_persistence_and_confirmation(client,monkeypatch):
    from src import llm,answer,hyde
    wid,headers=create(client);rule=seed(client,headers,wid)
    forbidden=Mock(side_effect=AssertionError('Provider must never be called'))
    for module in (llm,intelligence,answer,hyde):monkeypatch.setattr(module,'get_llm_client',forbidden)
    monkeypatch.setattr(llm.GroqProvider,'chat',forbidden);monkeypatch.setattr(llm.GeminiProvider,'chat',forbidden)
    ctx=personal.resolve(wid)
    snapshot=lambda:{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in ctx.root.rglob('*') if p.is_file()}
    before=snapshot();url=f'/api/personal/{wid}/whatif';body=request(rule)
    result=client.post(url,headers=headers,json=body);assert result.status_code==200,result.text
    assert result.json()['verdict']=='ineligible'
    assert result.json()['conditions'][0]['gap']['amount']=='5'
    for field in ['confirmed','applicability_confirmed']:
        result=client.post(url,headers=headers,json={**body,field:False}).json();assert result['verdict']=='insufficient evidence';assert result['conditions'][0]['gap'] is None
    mismatch={**body,'facts':[{'subject':'attendance','value':'70','unit':'marks'}]}
    assert client.post(url,headers=headers,json=mismatch).json()['verdict']=='insufficient evidence'
    assert client.post(url,headers=headers,json={**body,'facts':[]}).json()['verdict']=='insufficient evidence'
    other,foreign=create(client)
    assert client.post(url,headers=foreign,json=body).status_code==404
    assert client.post(f'/api/personal/{other}/whatif',headers=foreign,json=body).status_code==422
    assert client.post(url,json=body).status_code==404
    assert snapshot()==before
    assert forbidden.call_count==0


def test_conflicts_block_paths(monkeypatch):
    rules=[{'rule_id':str(i),'subject':'x','operator':'>=','value':str(v),'unit':'%','exceptions':[],'document_id':str(i),'chunk_id':str(i),'document':str(i),'page':1,'verbatim_quote':f'Minimum {v} percent.'} for i,v in enumerate([75,80])]
    monkeypatch.setattr(intelligence,'list_rules',lambda:rules)
    result=whatif.simulate(whatif.Scenario(facts=[{'subject':'x','value':'70','unit':'%'}],rule_ids=['0','1'],confirmed=True,applicability_confirmed=True))
    assert result['conflicted'] and result['verdict'] is None
    assert all(c['gap'] is None and c['counts'] is None for c in result['conditions'])


def test_fractional_threshold_precision():
    assert whatif.count_path('>=','75.5',60,90)['additional_completed']==33
    assert whatif.count_path('>=','75.000000000000000000000001',60,90)['additional_completed']==31


def test_whatif_dom():
    import subprocess
    result=subprocess.run(['node',str(Path(__file__).with_name('whatif_frontend.test.cjs'))],capture_output=True,text=True,timeout=20)
    assert result.returncode==0,result.stderr


def test_200_fractional_lower_bounds_against_integer_bruteforce():
    rng=random.Random(921)
    for _ in range(200):
        n=rng.randint(1,20);d=rng.randint(0,n);tenths=rng.randint(1,1000);op=rng.choice(['>=','>'])
        compare=intelligence.OPERATORS[op]
        expected=next((x for x in range(20001) if compare(1000*(d+x),tenths*(n+x))),None)
        actual=whatif.count_path(op,Decimal(tenths)/10,d,n)
        assert actual['additional_completed']==expected
