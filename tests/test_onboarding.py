"""Onboarding and publication regressions using temporary workspaces only."""
from fastapi.testclient import TestClient
from src import institutions,server


def test_public_empty_state_does_not_hide_private_admin_workspace():
    ctx=institutions.current();institutions.update_institution(ctx.institution_id,published=False)
    server._rate_windows.clear()
    with TestClient(server.app) as client:
        assert client.get('/institutions').json()=={'institutions':[]}
        assert client.get('/admin/institutions').status_code==401
        admin=client.get('/admin/institutions',headers={'Authorization':'Bearer isolated-test-admin'}).json()
        assert len(admin['institutions'])==1 and admin['institutions'][0]['institution_id']==ctx.institution_id
        assert not admin['institutions'][0]['published']


def test_create_by_name_generates_slug_without_duplicate_workspaces():
    server._rate_windows.clear()
    with TestClient(server.app,headers={'Authorization':'Bearer isolated-test-admin'}) as client:
        created=client.post('/admin/institutions',json={'name':'Synthetic Sample University'})
        assert created.status_code==200
        row=created.json();assert row['slug']=='synthetic-sample-university' and not row['published']
        assert client.post('/admin/institutions',json={'name':'  SYNTHETIC SAMPLE UNIVERSITY  '}).status_code==422
        assert sum(i['name']=='Synthetic Sample University' for i in client.get('/admin/institutions').json()['institutions'])==1


def test_non_ascii_institution_name_generates_safe_slug():
    row=institutions.create_institution('ಕಾಲ್ಪನಿಕ ಪರೀಕ್ಷಾ ಸಂಸ್ಥೆ')
    assert row['slug']=='institution' and not row['published']


def test_landing_exposes_separate_workflows_and_upload_guidance():
    with TestClient(server.app) as client:
        html=client.get('/').text
        for expected in ('id="view-home"','id="admin-institution"','id="institution"','id="upload-dropzone"',
                         'Upload & index PDFs','Unpublished','ADMIN_API_TOKEN','id="student-empty"','id="upload-progress"'):
            assert expected in html
        assert 'institution-slug' not in html
