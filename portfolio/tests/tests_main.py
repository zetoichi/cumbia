from django.core.exceptions import ImproperlyConfigured
from django.urls import resolve
from django.test import (
    TestCase,
)

from .mixins import GeneralCBVMixin
from ..views_main import (
    IndexView,
    PhDetailView,
)
from ..models import Photographer, Pic

class GeneralCBVTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Photographer.objects.create(
            first_name='First',
            last_name='Fake Ph'
        )
        Photographer.objects.create(
            first_name='Second',
            last_name='Fake Ph'
        )

class IndexTest(GeneralCBVMixin, GeneralCBVTestCase):
    url = '/'
    view_class = IndexView
    expected_template = 'portfolio/index.html'

    def test_index_displays_photographers(self):
        response = self.client.get('/')
        self.assertIn('First Fake Ph', response.content.decode())
        self.assertIn('Second Fake Ph', response.content.decode())

class PhDetailTest(GeneralCBVMixin, GeneralCBVTestCase):
    url = '/phs/1/'
    view_class = PhDetailView
    expected_template = 'portfolio/ph_detail.html'
