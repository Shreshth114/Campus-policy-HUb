"""Bounded FastEmbed calls preserve every vector and expose batch progress."""
import numpy as np
import pytest
from unittest.mock import MagicMock
from src import embeddings


def test_empty_input_does_not_load_model(monkeypatch):
    load=MagicMock(side_effect=AssertionError('Must not load an empty batch'))
    monkeypatch.setattr(embeddings,'_get_model',load)
    assert embeddings.embed_texts([])==[]
    load.assert_not_called()


def test_explicit_batch_size_preserves_all_vectors_and_order(monkeypatch,capsys):
    inputs=[f'Isolated embedding fixture {i}' for i in range(19)]
    expected=[np.array([float(i),1.0],dtype=np.float32) for i in range(19)]
    model=MagicMock()
    model.embed.return_value=iter(expected)
    monkeypatch.setattr(embeddings,'_get_model',lambda:model)
    monkeypatch.setattr(embeddings,'EMBED_BATCH_SIZE',8)
    result=embeddings.embed_texts(inputs)
    model.embed.assert_called_once_with(inputs,batch_size=8,parallel=None)
    assert result==[v.tolist() for v in expected]
    output=capsys.readouterr().out
    assert '8/19' in output and '16/19' in output and '19/19' in output
    assert 'chunks/s' in output


def test_model_failure_is_not_silently_skipped(monkeypatch):
    class Broken:
        def embed(self,texts,**kwargs):
            yield np.array([1.,0.])
            raise RuntimeError('fixture inference failure')
    monkeypatch.setattr(embeddings,'_get_model',lambda:Broken())
    with pytest.raises(RuntimeError,match='inference failure'):
        embeddings.embed_texts(['fixture a','fixture b'])


def test_missing_embedding_fails_count_check(monkeypatch):
    model=MagicMock()
    model.embed.return_value=iter([np.array([1.,0.])])
    monkeypatch.setattr(embeddings,'_get_model',lambda:model)
    with pytest.raises(ValueError,match='expected 2, got 1'):
        embeddings.embed_texts(['fixture a','fixture b'])


def test_invalid_batch_size_fails_explicitly(monkeypatch):
    monkeypatch.setattr(embeddings,'EMBED_BATCH_SIZE',0)
    with pytest.raises(ValueError,match='must be positive'):
        embeddings.embed_texts(['fixture'])
