from datetime import datetime, timezone

from django.contrib.auth.models import User
from freezegun import freeze_time
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from events.models import Event

TEST_USER_PASS = 'test-12345'


@freeze_time('2024-03-16 00:00:00')
class UnRegisterFromEventTests(APITestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create_user(username='u1', password=TEST_USER_PASS)
        u1_refresh = RefreshToken.for_user(self.u1)

        self.u2 = User.objects.create_user(username='u2', password=TEST_USER_PASS)

        self.u1_client = APIClient()
        self.u1_client.credentials(HTTP_AUTHORIZATION=f'JWT {u1_refresh.access_token}')

        t_past = datetime(2024, 3, 15, 0, 0, 0).replace(tzinfo=timezone.utc)
        t_future = datetime(2024, 3, 17, 0, 0, 0).replace(tzinfo=timezone.utc)

        self.past_evt = baker.make(Event, title='e1', organizer=self.u1, timestamp=t_past)
        self.future_evt = baker.make(Event, title='e2', organizer=self.u1, timestamp=t_future)

    def test_user_can_unregister_from_future_event(self):
        self.future_evt.attendees.add(self.u1)

        response = self.u1_client.post(
            f'/api/v1/events/{self.future_evt.id}/un-register/',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_unregister_from_past_event(self):
        self.future_evt.attendees.add(self.u1)

        response = self.u1_client.post(
            f'/api/v1/events/{self.past_evt.id}/un-register/',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['detail'], 'ACTION_NOT_ALLOWED_ON_PAST_EVENT')

    def test_user_cannot_unregister_from_non_published_event(self):
        self.future_evt.status = Event.Status.HIDDEN
        self.future_evt.save()
        self.future_evt.attendees.add(self.u1)

        response = self.u1_client.post(
            f'/api/v1/events/{self.future_evt.id}/un-register/',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['detail'], 'ACTION_NOT_ALLOWED_ON_NON_PUBLISHED_EVENT')

    def test_user_cannot_unregister_from_event_that_never_registered(self):
        response = self.u1_client.post(
            f'/api/v1/events/{self.future_evt.id}/un-register/',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['detail'], 'WAS_NOT_REGISTERED_TO_THIS_EVENT')

    def test_non_auth_user_cannot_unregister_from_event(self):
        response = self.client.post(
            f'/api/v1/events/{self.future_evt.id}/un-register/',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
