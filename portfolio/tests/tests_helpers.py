from django.test import (
    TestCase,
)

from core.helpers import get_first_from_pk_set

class HelpersTestCase(TestCase):

    def test_get_first_from_pk_set_true(self):
        pk_set = {1, 2, 3, 4, 5}

        pk = get_first_from_pk_set(pk_set)

        self.assertEqual(pk, 1)

    def test_get_first_from_pk_set_false(self):
        pk_set = {1, 2, 3, 4, 14}

        pk = get_first_from_pk_set(pk_set)

        self.assertNotEqual(pk, 14)
