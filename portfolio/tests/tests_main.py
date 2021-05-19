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
        cls.p1 = Photographer.objects.create(
            first_name='First',
            last_name='Fake Ph'
        )
        cls.p2 = Photographer.objects.create(
            first_name='Second',
            last_name='Fake Ph'
        )

    @classmethod
    def tearDownClass(cls):
        cls.p1.delete()
        cls.p2.delete()
        super().tearDownClass()

class IndexTest(GeneralCBVMixin, GeneralCBVTestCase):
    url = '/'
    view_class = IndexView
    expected_template = 'portfolio/index.html'

    def test_index_displays_photographers(self):
        response = self.client.get('/')
        self.assertIn('First Fake Ph', response.content.decode())
        self.assertIn('Second Fake Ph', response.content.decode())

class PhDetailTest(GeneralCBVMixin, GeneralCBVTestCase):
    url = '/phs/3/'
    view_class = PhDetailView
    expected_template = 'portfolio/ph_detail.html'
