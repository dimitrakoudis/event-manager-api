from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from events.models import Event

TEST_USER_PASS = 'test-12345'


class ListEventsTests(APITestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create_user(username='u1', password=TEST_USER_PASS)
        u1_refresh = RefreshToken.for_user(self.u1)

        self.u2 = User.objects.create_user(username='u2', password=TEST_USER_PASS)

        self.u1_client = APIClient()
        self.u1_client.credentials(HTTP_AUTHORIZATION=f'JWT {u1_refresh.access_token}')

        baker.make(Event, title='e1', organizer=self.u1)
        baker.make(Event, title='e2', organizer=self.u1)
        baker.make(Event, title='e3', organizer=self.u2)

    def test_user_can_list_all_events(self):
        response = self.u1_client.get(
            '/api/v1/events/',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 3)

    def test_user_can_list_only_mine_events(self):
        response = self.u1_client.get(
            '/api/v1/events/?only_mine=true',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)

    def test_non_auth_user_cannot_list_events(self):
        response = self.client.get(
            '/api/v1/events/',
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
