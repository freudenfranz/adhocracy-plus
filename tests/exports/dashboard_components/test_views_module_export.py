import pytest

from adhocracy4.dashboard import components
from apps.ideas.phases import CollectFeedbackPhase
from tests.helpers import setup_phase

component = components.modules.get('idea_export')


@pytest.mark.django_db
def test_edit_view(client, phase_factory):
    phase, module, project, item = setup_phase(
        phase_factory, None, CollectFeedbackPhase)
    initiator = module.project.organisation.initiators.first()
    url = component.get_base_url(module)
    client.login(username=initiator.email, password='password')
    response = client.get(url)
    assert response.status_code == 200
    assert 'export' in response.context
    assert 'comment_export' in response.context
    export_url = response.context['export']
    comment_export_url = response.context['comment_export']
    response = client.get(export_url)
    assert response.status_code == 200
    assert response.get('Content-Type') == \
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response = client.get(comment_export_url)
    assert response.status_code == 200
    assert response.get('Content-Type') == \
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
