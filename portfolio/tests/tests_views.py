import inspect

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

    # RESOLVE

    def test_index_url_should_resolve(self):
        url = '/'
        view_class = IndexView

        response = self.client.get(url)

        self.assertEqual(
            response.resolver_match.func.__name__,
            view_class.as_view().__name__
        )

    def test_ph_detail_url_should_resolve(self):
        ph = Photographer.objects.create(
            first_name='First',
            last_name='Fake Ph'
        )
        url = f'/phs/{ph.pk}/'
        view_class = PhDetailView

        response = self.client.get(url)

        expected = response.resolver_match.func.__name__
        actual = view_class.as_view().__name__
        self.assertEqual(expected, actual)

    # TEMPLATE

    def test_index_should_render_expected_template(self):
        url = '/'
        expected_template = 'portfolio/index.html'
        response = self.client.get(url)
        self.assertTemplateUsed(response, expected_template)

    def test_ph_detail_should_render_expected_template(self):
        ph = Photographer.objects.create(
            first_name='First',
            last_name='Fake Ph'
        )
        url = f'/phs/{ph.pk}/'
        view_class = PhDetailView
        expected_template = 'portfolio/ph_detail.html'

        response = self.client.get(url)

        self.assertTemplateUsed(response, expected_template)

    # CONTENT

    def test_index_should_display_photographers(self):
        ph_1 = Photographer.objects.create(
            first_name='Unique',
            last_name='Fake Ph'
        )
        ph_2 = Photographer.objects.create(
            first_name='Another',
            last_name='Fake Ph'
        )
        url = '/'

        response = self.client.get(url).content.decode()

        expected_1 = 'Unique Fake Ph'
        expected_2 = 'Another Fake Ph'
        self.assertIn(expected_1, response)
        self.assertIn(expected_2, response)
