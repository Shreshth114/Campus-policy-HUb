"""Scoring plumbing uses synthetic declarations, not actual human grades."""
from evaluation.ps1.refinements.review_evaluation import score
from tests.grounding_helpers import accepted_review
import json


def case(cid='a'):
    return {'id':cid,'question':'What is the charge?','chunks':[{'text':'R1. A charge of 41 credits applies.'}],
            'selection':{'status':'answer','claims':[{'source':'C1','provision':'P1'}]}}


def human(cid,acceptable):
    return {'case_id':cid,'source_pdf_checked':True,'human_reviewed':True,'review_origin':'human','reviewer':'SYNTHETIC TEST REVIEWER',
            'adjudication_status':'final','dimensions':{k:acceptable for k in ('relevant','complete','supported','qualifications_preserved')},
            'selection_acceptable':acceptable,'citation_correct':True,'appropriate_outcome':'answer' if acceptable else 'withhold',
            'notes':'Synthetic plumbing only','required_qualifications':[], 'atomic_requirements':['charge'],
            'supporting_provisions':[{'page':1,'quote':'Synthetic reference'}]}


def prediction(cid):return {'case_id':cid,'review':json.loads(accepted_review()),'usage':{'latency_ms':20,'input_tokens':30,'output_tokens':15,'reasoning_tokens':5}}


def test_pending_humans_never_create_accuracy():
    result=score([case()],[{'case_id':'a','human_reviewed':False}],[prediction('a')])
    assert result['human_scored_cases']==0 and result['false_approval_rate'] is None
    assert result['review_median_provider_latency_ms']==20
    assert result['reported_review_tokens']['output_tokens']==15
    assert not result['evaluation_complete']


def test_false_approval_and_rejection_have_distinct_denominators():
    bad=prediction('b');bad['review']['complete']=False
    result=score([case('a'),case('b')],[human('a',False),human('b',True)],[prediction('a'),bad])
    assert result['false_approval_rate']==1 and result['false_rejection_rate']==1
    assert result['acceptable_denominator']==1 and result['unacceptable_denominator']==1


def test_aggregate_booleans_cannot_override_invalid_coverage():
    p=prediction('a');p['review']['coverage'][0]['evidence']=['C9/P1']
    result=score([case()],[human('a',False)],[p])
    assert result['false_approval_rate']==0 and result['raw_boolean_false_approval_rate']==1


def test_provider_failure_not_counted_as_semantic_false_rejection():
    result=score([case()],[human('a',True)],[{'case_id':'a','error':'rate limited'}])
    assert result['service_error_cases']==1 and result['human_scored_cases']==0
    assert result['false_rejection_rate'] is None and result['review_observations']==0


def test_inconsistent_human_approval_stays_unscored():
    label=human('a',True);label['dimensions']['complete']=False
    result=score([case()],[label],[prediction('a')])
    assert result['human_scored_cases']==0


def test_null_dimensions_remain_unscored_instead_of_crashing():
    h=human('a',True);h['dimensions']=None
    assert score([case()],[h],[prediction('a')])['human_scored_cases']==0
