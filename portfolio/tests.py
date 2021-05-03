from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from .views import index
from .models import Photographer, Photo

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

class PhotographerAndPhotoModelsTest(TestCase):

    def test_saving_and_retrieving_photographer(self):
        ph = Photographer()
        ph.name = 'First Fake Ph'
        ph.save()
        
        photo_1 = Photo()
        photo_1.photographer = ph
        photo_1.url = 'photo_1.jpg'
        photo_1.save()
        
        photo_2 = Photo()
        photo_2.photographer = ph
        photo_2.url = 'photo_2.jpg'
        photo_2.save()

        saved_phs = Photographer.objects.all()
        self.assertEqual(saved_phs.count(), 1)

        saved_photos = Photo.objects.all()
        self.assertEqual(saved_photos.count(), 2)

        saved_photo_1 = saved_photos[0]
        saved_photo_2 = saved_photos[1]
        self.assertEqual(saved_photo_1.url, 'photo_1.jpg')
        self.assertEqual(saved_photo_1.photographer, ph)
        self.assertEqual(saved_photo_2.url, 'photo_2.jpg')
        self.assertEqual(saved_photo_2.photographer, ph)