import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from adhocracy4.projects.enums import Access
from adhocracy4.test.helpers import freeze_phase
from adhocracy4.test.helpers import redirect_target
from adhocracy4.test.helpers import setup_phase
from apps.mapideas import phases
from tests.helpers import assert_template_response


@pytest.mark.django_db
def test_detail_view_0(client, phase_factory, map_idea_factory, organisation):
    phase, module, project, item = setup_phase(
        phase_factory, map_idea_factory, phases.FeedbackPhase)
    url = item.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'a4_candy_mapideas/mapidea_detail.html')


@pytest.mark.django_db
def test_detail_view(client, phase_factory, map_idea_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.FeedbackPhase)
    url = mapidea.get_absolute_url()
    with freeze_phase(phase):
        response = client.get(url)
        assert_template_response(
            response, 'a4_candy_mapideas/mapidea_detail.html')
        assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view_private_not_visible_anonymous(client,
                                                   phase_factory,
                                                   map_idea_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.FeedbackPhase)
    mapidea.module.project.access = Access.PRIVATE
    mapidea.module.project.save()
    url = mapidea.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 302
    assert redirect_target(response) == 'account_login'


@pytest.mark.django_db
def test_detail_view_private_not_visible_normal_user(client,
                                                     user,
                                                     phase_factory,
                                                     map_idea_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.FeedbackPhase)
    mapidea.module.project.access = Access.PRIVATE
    mapidea.module.project.save()
    assert user not in mapidea.module.project.participants.all()
    client.login(username=user.email,
                 password='password')
    url = mapidea.get_absolute_url()
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_detail_view_private_visible_to_participant(client,
                                                    user,
                                                    phase_factory,
                                                    map_idea_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.FeedbackPhase)
    mapidea.module.project.access = Access.PRIVATE
    mapidea.module.project.save()
    url = mapidea.get_absolute_url()
    assert user not in mapidea.module.project.participants.all()
    mapidea.module.project.participants.add(user)
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view_private_visible_to_moderator(client,
                                                  phase_factory,
                                                  map_idea_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.FeedbackPhase)
    mapidea.module.project.access = Access.PRIVATE
    mapidea.module.project.save()
    url = mapidea.get_absolute_url()
    user = mapidea.project.moderators.first()
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view_private_visible_to_initiator(client,
                                                  phase_factory,
                                                  map_idea_factory):
    phase, module, project, mapidea = setup_phase(
        phase_factory, map_idea_factory, phases.FeedbackPhase)
    mapidea.module.project.access = Access.PRIVATE
    mapidea.module.project.save()
    url = mapidea.get_absolute_url()
    user = mapidea.project.organisation.initiators.first()
    client.login(username=user.email,
                 password='password')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_view_semipublic_participation_only_participant(
        client, user, phase_factory, map_idea_factory):
    phase, module, project, map_idea = setup_phase(
        phase_factory, map_idea_factory, phases.FeedbackPhase)
    map_idea.module.project.access = Access.SEMIPUBLIC
    map_idea.module.project.save()

    url = map_idea.get_absolute_url()
    map_idea_ct = ContentType.objects.get_for_model(type(map_idea))
    api_url = reverse('comments-list',
                      kwargs={
                          'content_type': map_idea_ct.pk,
                          'object_pk': map_idea.pk
                      })
    comment_data = {
        'comment': 'no comment',
    }

    with freeze_phase(phase):
        response = client.get(url)
        assert response.status_code == 200
        assert_template_response(response,
                                 'a4_candy_mapideas/mapidea_detail.html')
        response = client.post(api_url, comment_data, format='json')

        assert response.status_code == 403

        client.login(username=user.email, password='password')

        response = client.get(url)
        assert response.status_code == 200
        assert_template_response(response,
                                 'a4_candy_mapideas/mapidea_detail.html')
        response = client.post(api_url, comment_data, format='json')
        assert response.status_code == 403

        map_idea.module.project.participants.add(user)

        response = client.get(url)
        assert response.status_code == 200
        assert_template_response(response,
                                 'a4_candy_mapideas/mapidea_detail.html')
        response = client.post(api_url, comment_data, format='json')
        assert response.status_code == 201
