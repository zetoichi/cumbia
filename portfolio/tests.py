from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from .views import index

class IndexTest(TestCase):

    def test_root_url_resolves_to_index(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_home_returns_correct_html(self):
        request = HttpRequest()
        response = index(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>Cumbia</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))