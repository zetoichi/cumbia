from django.urls import resolve
from django.test import (
    TestCase,
)
from django.http import HttpRequest
from django.template.loader import render_to_string

from .public_views import PublicIndexView
from .dash_views import DashIndexView
from .models import Photographer, Pic

class PublicIndexTest(TestCase):

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

    def test_root_url_resolves_to_index(self):
        response = self.client.get('/')
        self.assertEqual(
            response.resolver_match.func.__name__,
            PublicIndexView.as_view().__name__
        )

    def test_uses_public_index_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'portfolio/public_index.html')

    def test_index_displays_photographers(self):
        response = self.client.get('/')
        self.assertIn('First Fake Ph', response.content.decode())
        self.assertIn('Second Fake Ph', response.content.decode())

class DashIndexTest(TestCase):

    def test_dash_url_resolves_to_dashboard(self):
        response = self.client.get('/dash/')
        self.assertEqual(
            response.resolver_match.func.__name__,
            DashIndexView.as_view().__name__
        )

    def test_uses_dash_index_template(self):
        response = self.client.get('/dash/')
        self.assertTemplateUsed(response, 'portfolio/dash_index.html')


# class PhotographerAndPhotoModelsTest(TestCase):

#     def test_saving_and_retrieving_photographer(self):
#         ph = Photographer()
#         ph.name = 'First Fake Ph'
#         ph.save()

#         photo_1 = Pic()
#         photo_1.photographer = ph
#         photo_1.url = 'photo_1.jpg'
#         photo_1.save()

#         photo_2 = Pic()
#         photo_2.photographer = ph
#         photo_2.url = 'photo_2.jpg'
#         photo_2.save()

#         saved_phs = Photographer.objects.all()
#         self.assertEqual(saved_phs.count(), 1)

#         saved_photos = Pic.objects.all()
#         self.assertEqual(saved_photos.count(), 2)

#         saved_photo_1 = saved_photos[0]
#         saved_photo_2 = saved_photos[1]
#         self.assertEqual(saved_photo_1.url, 'photo_1.jpg')
#         self.assertEqual(saved_photo_1.photographer, ph)
#         self.assertEqual(saved_photo_2.url, 'photo_2.jpg')
#         self.assertEqual(saved_photo_2.photographer, ph)

# # EXPECTED FAILURE: view/url/template need to be created
# class PhotographerViewTest(TestCase):

#     def test_uses_photographer_template(self):
#         ph = Photographer.objects.create()
#         response = self.client.get(f'/phs/{ph.id}')
#         self.assertTemplateUsed(response, 'portfolio/photographer.html')
