import pytest
from src.mcp_server import scoped_search
from src.institutions import current
from tests.test_personal import client,create,uploaded

@pytest.mark.asyncio
async def test_mcp_bound_search_is_personal_only_and_has_no_secret_metadata(client):
    wid,headers=create(client);uploaded(client,headers)
    result=await scoped_search(wid,'attendance','raw',5)
    assert result['chunks'] and result['chunks'][0]['page']==1
    assert 'workspace_id' not in str(result) and 'source_path' not in str(result)
    other,_=create(client);assert not (await scoped_search(other,'attendance'))['chunks']
    with pytest.raises(ValueError):await scoped_search(current().institution_id,'attendance')
    with pytest.raises(ValueError):await scoped_search(wid,'')
    with pytest.raises(ValueError):await scoped_search(wid,'q',top_k=999)
