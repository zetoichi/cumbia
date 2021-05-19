from django.core.exceptions import ImproperlyConfigured
from django.urls import resolve
from django.test import (
    TestCase,
)

from portfolio.views_main import (
    IndexView,
    PhDetailView,
)
from portfolio.models import Photographer, Pic

class GeneralCBVTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.p1 = Photographer.objects.create(
            first_name='First',
            last_name='Fake Ph'
        )
        print(cls.p1)
        cls.p2 = Photographer.objects.create(
            first_name='Second',
            last_name='Fake Ph'
        )
        print(cls.p2)

    @classmethod
    def tearDownClass(cls):
        cls.p1.delete()
        cls.p2.delete()
        super().tearDownClass()

    # RESOLVERS

    def test_index_url_resolves(self):
        url = '/'
        view_class = IndexView
        response = self.client.get(url)
        self.assertEqual(
            response.resolver_match.func.__name__,
            view_class.as_view().__name__
        )

    def test_index_uses_expected_template(self):
        url = '/'
        expected_template = 'portfolio/index.html'
        response = self.client.get(url)
        self.assertTemplateUsed(response, expected_template)

    def test_ph_detail_url_resolves(self):
        url_1 = '/phs/1/'
        url_2 = '/phs/2/'
        view_class = PhDetailView

        response_1 = self.client.get(url_1)
        response_2 = self.client.get(url_2)
        expected_1 = response_1.resolver_match.func.__name__
        expected_2 = response_2.resolver_match.func.__name__
        actual_1 = view_class.as_view().__name__
        actual_2 = view_class.as_view().__name__
        self.assertEqual(expected_1, actual_1)
        self.assertEqual(expected_2, actual_2)

    def test_ph_detail_uses_expected_template(self):
        url_1 = '/phs/1/'
        url_2 = '/phs/2/'
        expected_template = 'portfolio/ph_detail.html'

        response_1 = self.client.get(url_1)
        response_2 = self.client.get(url_2)
        self.assertTemplateUsed(response_1, expected_template)
        self.assertTemplateUsed(response_2, expected_template)

    # CONTENT

    def test_index_displays_photographers(self):
        url = '/'
        response = self.client.get(url).content.decode()
        expected_1 = 'First Fake Ph'
        expected_2 = 'Second Fake Ph'
        self.assertIn(expected_1, response)
        self.assertIn(expected_2, response)
