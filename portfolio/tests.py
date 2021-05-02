from django.urls import resolve
from django.test import TestCase
from .views import home

class HomepageTest(TestCase):

    def test_root_url_resolves_to_home(self):
        found = resolve('/')
        self.assertEqual(found.func, home)