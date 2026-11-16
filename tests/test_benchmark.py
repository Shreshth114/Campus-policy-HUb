"""Metric arithmetic on isolated fixture observations, never university accuracy."""
import json
from unittest.mock import AsyncMock
from types import SimpleNamespace
import pytest
from bench import run_benchmark as bench
from src.retrieve import RetrievalResult
from src.trace import Trace,ChunkTrace
from tests.test_guardrails import make_chunk
from src.institutions import workspace_path,current


def query(id='fixture-q',verified=False,gold=None,**extra):
    return {'id':id,'query':'Synthetic fixture marker query','gold_chunk_ids':gold or ['a','b'],
            'labels_verified':verified,'institution_id':current().institution_id,**extra}


@pytest.mark.asyncio
async def test_true_recall_and_hit_rate_differ(monkeypatch):
    fake=AsyncMock(return_value=RetrievalResult(chunks=[make_chunk('a'),make_chunk('x'),make_chunk('b')],
                                               timings_ms={'total':12}))
    monkeypatch.setattr(bench,'retrieve',fake)
    result=await bench.evaluate_retrieval([query(is_synthetic=True)],'raw',synthetic=True)
    assert result['recall_at_1']==.5 and result['hit_at_1']==1
    assert result['recall_at_3']==1 and result['mrr']==1
    assert result['mean_latency_ms']==12
    assert fake.call_args.kwargs['production'] is False


@pytest.mark.asyncio
async def test_unverified_labels_skip_all_calls(monkeypatch):
    fake=AsyncMock(side_effect=AssertionError('unverified labels must not be scored'))
    monkeypatch.setattr(bench,'retrieve',fake)
    result=await bench.evaluate_retrieval([query()],'raw')
    assert result['recall_at_5'] is None and result['n_queries']==0
    fake.assert_not_called()


@pytest.mark.asyncio
async def test_missing_queries_produce_no_measurements(monkeypatch,tmp_path):
    path=workspace_path('queries')
    path.write_text(json.dumps(query())+'\n')
    monkeypatch.setattr(bench,'QUERIES_PATH',path)
    monkeypatch.setattr(bench,'RESULTS_DIR',tmp_path/'results')
    fake=AsyncMock(side_effect=AssertionError('No pipeline calls'))
    monkeypatch.setattr(bench,'ask',fake)
    result=await bench.run_benchmark()
    assert result['metadata']['status']=='awaiting_verified_labels'
    assert result['metadata']['labels_verified'] is False
    assert result['retrieval_metrics']=={}
    assert 'no measurements' in (workspace_path('results')/'latest.svg').read_text().lower()
    assert 'No accuracy measurements' in (workspace_path('results')/'latest.md').read_text()
    assert json.loads(path.read_text())['labels_verified'] is False
    fake.assert_not_called()


@pytest.mark.asyncio
async def test_failed_retrieval_is_reported_not_hidden(monkeypatch):
    monkeypatch.setattr(bench,'retrieve',AsyncMock(side_effect=RuntimeError('fixture failure')))
    result=await bench.evaluate_retrieval([query(is_synthetic=True)],'raw',synthetic=True)
    assert result['errors']==1 and result['n_queries']==1 and result['mrr']==0
    assert result['observations'][0]['error']=='RuntimeError'


@pytest.mark.asyncio
async def test_infrastructure_abstain_not_counted_as_correct(monkeypatch):
    monkeypatch.setattr(bench,'ask',AsyncMock(return_value=Trace(question='fixture',mode='raw',
                         decision='abstained',error='provider unavailable')))
    q=query(verified=True,expect='abstain')
    q['gold_chunk_ids']=[]
    result=await bench.evaluate_safety([q],'raw')
    assert result['errors']==1 and result['oos_correct']==0


@pytest.mark.asyncio
async def test_safety_checks_all_citations_not_only_nonempty(monkeypatch):
    trace=Trace(question='fixture',mode='raw',decision='answered',citations=['missing'],
                retrieved=[ChunkTrace('a','Fixture','1',0,.9,'Fixture',approved=True)])
    monkeypatch.setattr(bench,'ask',AsyncMock(return_value=trace))
    result=await bench.evaluate_safety([query(verified=True)],'raw')
    assert result['citation_validity_rate']==0


def test_threshold_sweep_uses_cosine_not_rrf():
    result=bench.threshold_sweep([{'best_similarity':.1,'gold_hit':False,'rrf_score':1.0}],(.35,))
    assert result[0]['retrieval_acceptance_rate']==0
    assert result[0]['accepted_without_gold_rate'] is None


@pytest.mark.parametrize('records',[
    [{'id':'a','query':'x','gold_chunk_ids':'bad'}],
    [{'id':'a','query':'x'},{'id':'a','query':'y'}],
    [{'id':'a','query':' '}],
    [{'id':'a','query':'x','labels_verified':'true'}],
])
def test_bad_labels_rejected(monkeypatch,tmp_path,records):
    path=workspace_path('queries')
    path.write_text('\n'.join(json.dumps(r) for r in records))
    monkeypatch.setattr(bench,'QUERIES_PATH',path)
    with pytest.raises(ValueError): bench.load_queries()


@pytest.mark.asyncio
async def test_no_cache_flag_reaches_hyde_context(monkeypatch,tmp_path):
    # Supplied verification state is only mocked in memory, never written as labels.
    q=query(verified=True,gold=['a'])
    monkeypatch.setattr(bench,'load_queries',lambda:[q])
    monkeypatch.setattr(bench,'RESULTS_DIR',tmp_path/'results')
    observed=[]
    monkeypatch.setattr(bench,'has_chunks',lambda:True)
    monkeypatch.setattr(bench,'valid_cached_citations',lambda ids:True)
    async def search(*args,**kwargs):
        observed.append(bench.cache_enabled.get())
        return RetrievalResult(chunks=[make_chunk('a')])
    monkeypatch.setattr(bench,'retrieve',search)
    monkeypatch.setattr(bench,'ask',AsyncMock(return_value=Trace(question='fixture',mode='raw',decision='abstained')))
    await bench.run_benchmark(['raw'],use_cache=False)
    assert observed==[False]


def test_svg_escapes_mode_and_ignores_absent_numbers():
    result={'retrieval_metrics':{'<script>':{'recall_at_5':None,'mrr':.5}}}
    svg=bench.generate_svg(result)
    assert '<script>' not in svg and '&lt;script&gt;' in svg


@pytest.mark.asyncio
async def test_verified_labels_without_real_corpus_still_block_metrics(monkeypatch,tmp_path):
    monkeypatch.setattr(bench,'load_queries',lambda:[query(verified=True)])
    monkeypatch.setattr(bench,'RESULTS_DIR',tmp_path/'results')
    fake=AsyncMock(side_effect=AssertionError('No corpus means no accuracy claim'))
    monkeypatch.setattr(bench,'retrieve',fake)
    result=await bench.run_benchmark()
    assert result['metadata']['status']=='awaiting_approved_corpus'
    assert not result['retrieval_metrics']
    fake.assert_not_called()


def test_paired_raw_hyde_counts_real_wins_ties_losses_and_excludes_fallback():
    def row(i,rr,**extra):return {'id':i,'reciprocal_rank':rr,'recall_at_3':int(rr>0),'error':None,**extra}
    metrics={'raw':{'observations':[row('win',.5),row('tie',1),row('loss',1),row('fallback',0),row('missing',1)]},
             'hyde':{'observations':[row('win',1),row('tie',1),row('loss',.5),row('fallback',1,hyde_failed=True)]}}
    result=bench.paired_raw_hyde(metrics)
    assert (result['n_pairs'],result['wins'],result['ties'],result['losses'])==(3,1,1,1)
    assert result['mean_rr_delta']==0
    assert {r['reason'] for r in result['excluded']}=={'hyde_fell_back_to_raw','missing_mode_result'}


def test_empty_pairs_never_report_zero_as_measured_accuracy():
    result=bench.paired_raw_hyde({})
    assert result['n_pairs']==0 and result['mean_rr_delta'] is None


@pytest.mark.asyncio
async def test_observations_preserve_actual_hyde_and_rank(monkeypatch):
    monkeypatch.setattr(bench,'retrieve',AsyncMock(return_value=RetrievalResult(chunks=[make_chunk('x'),make_chunk('a')],hyde_text='Synthetic search key',llm_usage={'hyde':{'input_tokens':12}})))
    result=await bench.evaluate_retrieval([query(is_synthetic=True)],'hyde',synthetic=True)
    row=result['observations'][0]
    assert row['reciprocal_rank']==.5 and row['recall_at_3']==.5
    assert row['hyde_text']=='Synthetic search key' and row['llm_usage']['hyde']['input_tokens']==12


@pytest.mark.parametrize('fallback',[False,True])
@pytest.mark.asyncio
async def test_ties_or_fallback_never_declare_unique_best_mode(monkeypatch,fallback):
    monkeypatch.setattr(bench,'load_queries',lambda:[query(verified=True,gold=['a'])])
    monkeypatch.setattr(bench,'has_chunks',lambda:True)
    monkeypatch.setattr(bench,'valid_cached_citations',lambda ids:True)
    async def search(question,mode,**kwargs):
        return RetrievalResult(chunks=[make_chunk('a')],hyde_failed=fallback and mode=='hyde')
    monkeypatch.setattr(bench,'retrieve',search)
    monkeypatch.setattr(bench,'evaluate_safety',AsyncMock(return_value={'errors':0}))
    monkeypatch.setattr(bench,'evaluate_decoy_isolation',AsyncMock(return_value=[]))
    result=await bench.run_benchmark(['raw','hyde'],use_cache=False)
    assert result['metadata']['best_mode'] is None
    assert result['metadata']['status']==('completed_with_errors' if fallback else 'completed')
    assert result['raw_hyde_comparison']['n_pairs']==(0 if fallback else 1)
