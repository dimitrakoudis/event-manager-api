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