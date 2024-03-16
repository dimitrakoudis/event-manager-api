from unittest.mock import Mock

from django.contrib.auth.models import User
from model_bakery import baker
from rest_framework.test import APITestCase

from events.models import Event
from events.serializers import EventSerializer


class EventSerializerTests(APITestCase):
    def setUp(self) -> None:
        self.minimum_valid_data = {
            "title": "Test event",
            "place": "Any place",
            "timestamp": "2050-12-30T00:00:01.973Z",
        }

    def test_can_serialize_objects(self):
        objs = [
            baker.make(Event, id=1, title='e1'),
        ]
        serializer = EventSerializer(objs, many=True)

        self.assertEqual(
            sorted(list(serializer.data[0].keys())),
            sorted([
                'id', 'title', 'organizer', 'status', 'place', 'timestamp',
                'description', 'attendees', 'created_at', 'updated_at',
            ])
        )

    def test_can_deserialize_objects(self):
        serializer = EventSerializer(data=self.minimum_valid_data)

        self.assertTrue(serializer.is_valid())
        self.assertDictEqual(serializer.errors, {})

    def test_save_create_new_instance(self):
        self.minimum_valid_data['title'] = 'testing-create'
        request_user = baker.make(User)

        mocked_request = Mock()
        mocked_request.user.id = request_user.id
        serializer = EventSerializer(data=self.minimum_valid_data, context={'request': mocked_request})

        serializer.is_valid()
        new_event = serializer.save()
        self.assertEqual(new_event.title, 'testing-create')

    def test_save_update_existing_instance(self):
        self.minimum_valid_data['title'] = 'testing-update'

        event = baker.make(Event, title='initial-title')
        serializer = EventSerializer(event, data=self.minimum_valid_data)

        serializer.is_valid()
        new_invoice = serializer.save()
        self.assertEqual(new_invoice.title, 'testing-update')
