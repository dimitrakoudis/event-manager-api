from django.test import TestCase
from model_bakery import baker

from events.models import Category


class CategoryTests(TestCase):
    def test_can_create_obj(self):
        obj = baker.make(Category)

        self.assertIsInstance(obj.id, int)
        self.assertIsInstance(obj.name, str)

    def test_str(self):
        obj = baker.make(Category, name='c1')

        actual = str(obj)
        expected = 'c1'
        self.assertEqual(actual, expected)
