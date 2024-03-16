from django.contrib.auth.models import User
from django.test import TestCase
from model_bakery import baker

from events.models import Event


class EventTests(TestCase):
    def test_can_create_obj(self):
        obj = baker.make(Event)

        self.assertIsInstance(obj.id, int)
        self.assertIsInstance(obj.title, str)

    def test_str(self):
        obj = baker.make(Event, title='e1')

        actual = str(obj)
        expected = 'e1'
        self.assertEqual(actual, expected)

    def test_attendees_count(self):
        obj = baker.make(Event)
        attendees = [baker.make(User), baker.make(User), ]

        obj.attendees.add(*attendees)

        actual = obj.attendees_count
        expected = 2
        self.assertEqual(actual, expected)

    def test_attendees_count_zero(self):
        obj = baker.make(Event)

        actual = obj.attendees_count
        expected = 0
        self.assertEqual(actual, expected)
