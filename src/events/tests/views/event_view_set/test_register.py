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
class RegisterToEventTests(APITestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create_user(username='u1', password=TEST_USER_PASS)
        u1_refresh = RefreshToken.for_user(self.u1)

        self.u2 = User.objects.create_user(username='u2', password=TEST_USER_PASS)

        self.u1_client = APIClient()
        self.u1_client.credentials(HTTP_AUTHORIZATION=f'JWT {u1_refresh.access_token}')

        t_past = datetime(2024, 3, 15, 0, 0, 0).replace(tzinfo=timezone.utc)
        t_future = datetime(2024, 3, 17, 0, 0, 0).replace(tzinfo=timezone.utc)

        self.past_evt = baker.make(Event, title='e1', organizer=self.u1, timestamp=t_past)
        self.future_evt_1 = baker.make(Event, title='e2', organizer=self.u1, timestamp=t_future)
        self.future_evt_2 = baker.make(Event, title='e3', organizer=self.u2, timestamp=t_future)

    def test_user_can_register_to_future_event(self):
        response = self.u1_client.post(
            f'/api/v1/events/{self.future_evt_2.id}/register/',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_can_register_to_event_that_organized(self):
        response = self.u1_client.post(
            f'/api/v1/events/{self.future_evt_1.id}/register/',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_non_auth_user_cannot_register_to_event(self):
        response = self.client.post(
            f'/api/v1/events/{self.future_evt_2.id}/register/',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
