from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from events.models import Event

TEST_USER_PASS = 'test-12345'


class UpdateEventTests(APITestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create_user(username='u1', password=TEST_USER_PASS)
        u1_refresh = RefreshToken.for_user(self.u1)

        self.u2 = User.objects.create_user(username='u2', password=TEST_USER_PASS)

        self.u1_client = APIClient()
        self.u1_client.credentials(HTTP_AUTHORIZATION=f'JWT {u1_refresh.access_token}')

        self.e1 = baker.make(Event, title='e1', organizer=self.u1)
        self.e2 = baker.make(Event, title='e2', organizer=self.u2)

    def test_user_can_update_event_that_is_organizer(self):
        response = self.u1_client.put(
            f'/api/v1/events/{self.e1.id}/',
            format='json',
            data={
                "title": "dummy-evt",
                "status": "PUBLISHED",
                "place": "any place",
                "timestamp": "2025-12-01T00:00:00Z",
                "description": "...",
                "capacity": 123,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_event_that_is_not_organizer(self):
        response = self.u1_client.put(
            f'/api/v1/events/{self.e2.id}/',
            format='json',
            data={},
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_non_auth_user_cannot_update_event(self):
        response = self.client.put(
            f'/api/v1/events/{self.e1.id}/',
            format='json',
            data={},
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
