from django.core.exceptions import ImproperlyConfigured
from django.urls import resolve
from django.test import (
    TestCase,
)
from django.http import HttpRequest
from django.template.loader import render_to_string

from .mixins import GeneralCBVMixin
from ..views_public import PublicIndexView
from ..views_dash import (
    DashIndexView,
    DashAddPicsView,
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

class PublicIndexTest(GeneralCBVMixin, GeneralCBVTestCase):
    url = '/'
    view_class = PublicIndexView
    expected_template = 'portfolio/public_index.html'

    def test_index_displays_photographers(self):
        response = self.client.get('/')
        self.assertIn('First Fake Ph', response.content.decode())
        self.assertIn('Second Fake Ph', response.content.decode())

class DashIndexTest(GeneralCBVMixin, GeneralCBVTestCase):
    url = '/dash/'
    view_class = DashIndexView
    expected_template = 'portfolio/dash_index.html'

class DashAddPicsTest(GeneralCBVMixin, GeneralCBVTestCase):
    url = '/dash/phs/add/1/'
    view_class = DashAddPicsView
    expected_template = 'portfolio/dash_add_pics.html'
