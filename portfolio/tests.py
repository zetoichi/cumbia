from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from .views import index
from .models import Photographer

class IndexTest(TestCase):

    def test_root_url_resolves_to_index(self):
        found = resolve('/')
        self.assertEqual(found.func, index)

    def test_uses_index_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'portfolio/index.html')

    def test_index_displays_photographers(self):
        Photographer.objects.create(name='First Fake Ph')
        Photographer.objects.create(name='Second Fake Ph')

        response = self.client.get('/')
        
        self.assertIn('First Fake Ph', response.content.decode())
        self.assertIn('Second Fake Ph', response.content.decode())

class PhotographerModelTest(TestCase):

    def test_saving_and_retrieving_photographer(self):
        first_ph = Photographer()
        first_ph.name = 'First Fake Ph'
        first_ph.save()
        
        second_ph = Photographer()
        second_ph.name = 'Second Fake Ph'
        second_ph.save()

        saved_phs = Photographer.objects.all()
        self.assertEqual(saved_phs.count(), 2)

        first_saved_ph = saved_phs[0]
        second_saved_ph = saved_phs[1]
        self.assertEqual(first_saved_ph.name, 'First Fake Ph')
        self.assertEqual(second_saved_ph.name, 'Second Fake Ph')