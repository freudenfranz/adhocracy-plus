import pytest

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import redirect_target
from apps.debate import phases
from tests.helpers import assert_template_response
from tests.helpers import freeze_phase
from tests.helpers import setup_phase


@pytest.mark.django_db
def test_detail_view(client, phase_factory, subject_factory):
    phase, module, project, subject = setup_phase(
        phase_factory, subject_factory, phases.DebatePhase)
    url = subject.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'a4_candy_debate/subject_detail.html')
        assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrized('subject__module__project__is_public', [False])
def test_detail_view_private_not_visible_anonymous(client,
                                                   phase_factory,
                                                   subject_factory):
    phase, module, project, subject = setup_phase(
        phase_factory, subject_factory, phases.DebatePhase)
    subject.module.project.access = Access.PRIVATE
    subject.module.project.save()
    url = subject.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'


@pytest.mark.django_db
@pytest.mark.parametrized('subject__module__project__is_public', [False])
def test_detail_view_private_not_visible_normal_user(client,
                                                     user,
                                                     phase_factory,
                                                     subject_factory):
    phase, module, project, subject = setup_phase(
        phase_factory, subject_factory, phases.DebatePhase)
    subject.module.project.access = Access.PRIVATE
    subject.module.project.save()
    assert user not in subject.module.project.participants.all()
    client.login(username=user.email,
                 password='password')
    url = subject.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrized('subject__module__project__is_public', [False])
def test_detail_view_private_visible_to_participant(client,
                                                    user,
                                                    phase_factory,
                                                    subject_factory):
    phase, module, project, subject = setup_phase(
        phase_factory, subject_factory, phases.DebatePhase)
    subject.module.project.access = Access.PRIVATE
    subject.module.project.save()
    url = subject.get_absolute_url()
    assert user not in subject.module.project.participants.all()
    subject.module.project.participants.add(user)
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrized('subject__module__project__is_public', [False])
def test_detail_view_private_visible_to_moderator(client,
                                                  phase_factory,
                                                  subject_factory):
    phase, module, project, subject = setup_phase(
        phase_factory, subject_factory, phases.DebatePhase)
    subject.module.project.access = Access.PRIVATE
    subject.module.project.save()
    url = subject.get_absolute_url()
    user = subject.project.moderators.first()
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrized('subject__module__project__is_public', [False])
def test_detail_view_private_visible_to_initiator(client,
                                                  phase_factory,
                                                  subject_factory):
    phase, module, project, subject = setup_phase(
        phase_factory, subject_factory, phases.DebatePhase)
    subject.module.project.access = Access.PRIVATE
    subject.module.project.save()
    url = subject.get_absolute_url()
    user = subject.project.organisation.initiators.first()
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200
