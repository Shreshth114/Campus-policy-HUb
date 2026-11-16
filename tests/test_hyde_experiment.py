"""Pure local checks for the disposable experiment; no provider or store access."""
import math
import pytest
from improve_hyde.experiment import average, key, normalized


def test_normalization_and_query_weight():
    assert normalized([3,4]) == [.6,.8]
    assert average([[10,0],[0,1]],[1,1]) == pytest.approx([2**-.5,2**-.5])
    weighted=average([[10,0],[0,1]],[2,1])
    assert weighted[0]/weighted[1] == pytest.approx(2)
    assert sum(x*x for x in weighted) == pytest.approx(1)


@pytest.mark.parametrize('vectors,weights', [([],[]),([[0,0]],[1]),([[1,0],[1]],[1,1]),([[1,0]],[0]),([[math.nan,0]],[1])])
def test_invalid_vector_inputs_rejected(vectors,weights):
    with pytest.raises(ValueError): average(vectors,weights)


def test_cache_separates_variant_prompt_and_question():
    values=[key('v1','prompt','question'),key('v2','prompt','question'),key('v1','changed','question'),key('v1','prompt','changed')]
    assert len(set(values))==4
    assert key('v1','prompt','question')==values[0]


def test_empty_provider_response_is_failure_and_never_cached(tmp_path,monkeypatch):
    import asyncio,json
    import improve_hyde.experiment as experiment
    from src.llm import GroqProvider
    (tmp_path/'results').mkdir();(tmp_path/'cache').mkdir()
    monkeypatch.setattr(experiment,'OUT',tmp_path)
    async def empty(self,**kwargs):raise ValueError('Provider returned empty content')
    async def no_wait(seconds):pass
    monkeypatch.setattr(GroqProvider,'chat',empty)
    monkeypatch.setattr(asyncio,'sleep',no_wait)
    with pytest.raises(ValueError):asyncio.run(experiment.completion('v2','prompt','question'))
    failures=[json.loads(line) for line in (tmp_path/'results/provider_failures.jsonl').read_text().splitlines()]
    assert len(failures)==4
    assert all(row['status'] is None and row['details']['error']=='ValueError' for row in failures)
    assert not list((tmp_path/'cache').glob('*.json'))
