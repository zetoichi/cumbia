import inspect

from django.urls import resolve
from django.test import (
    TestCase,
)

from portfolio.views_main import (
    IndexView,
    PhDetailView,
)
from portfolio.views_json import save_new_pics
from portfolio.models import Photographer, Pic

class CBVTestCase(TestCase):

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
            first_name='Silvester',
            last_name='Stallone'
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
            first_name='Jean Claude',
            last_name='Van Damme'
        )
        url = f'/phs/{ph.pk}/'
        view_class = PhDetailView
        expected_template = 'portfolio/ph_detail.html'

        response = self.client.get(url)

        self.assertTemplateUsed(response, expected_template)

    # CONTENT

    def test_index_should_display_photographers(self):
        ph_1 = Photographer.objects.create(
            first_name='Steven',
            last_name='Seagal'
        )
        ph_2 = Photographer.objects.create(
            first_name='Arnold',
            last_name='Schwarzenegger',
            display_name='Arnie'
        )
        url = '/'

        response = self.client.get(url).content.decode()

        expected_1 = 'Steven Seagal'
        expected_2 = 'Arnie'
        self.assertIn(expected_1, response)
        self.assertIn(expected_2, response)

class JSONViewsTestCase(TestCase):

    test_image_files = {
        'portrait': 'ozFsMoAW_testpic_portrait.jpg',
        'landscape': 'BreHayL8_testpic_landscape.jpg',
        'big': '4wmdrys5_testpic_big.jpg',
    }

    def test_save_pics_url_should_resolve(self):
        url = '/phs/savepics/1/'
        view_func = save_new_pics

        response = self.client.get(url)

        self.assertEqual(response.resolver_match.func, view_func)

    # def test_save_pics_should_create_pic_objects(self):
    #     test_file = self.test_image_files.get('landscape')
    #     ph = Photographer.objects.create(
    #         first_name='Jason',
    #         last_name='Statham'
    #     )
    #     url = f'/phs/savepics/{ph.pk}/'
    #     response = self.client.post(url)

    #     self.assertEqual(response, {'jason': 'statham'})
