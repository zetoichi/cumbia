from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from .views import home

class HomepageTest(TestCase):

    def test_root_url_resolves_to_home(self):
        found = resolve('/')
        self.assertEqual(found.func, home)

    def test_home_returns_correct_html(self):
        request = HttpRequest()
        response = home(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Cumbia</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))