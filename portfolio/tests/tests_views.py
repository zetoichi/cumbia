import os
import json
import inspect
from unittest.mock import Mock, patch

from django.urls import resolve, reverse
from django.test import (
    TestCase,
)

from portfolio.views_auth import (
    CumbiaLoginView,
    cumbia_logout,
)
from portfolio.views_main import (
    IndexView,
    AboutView,
    ContactView,
    PhCreateView,
    PhCreateConfirmView,
    PhDetailView,
    PhAddPicsView,
    PhAddFirstPicsView,
)
from portfolio.views_json import (
    save_new_pics,
    sort_ph,
    sort_pic,
)
from portfolio.models import Photographer, Pic
from .helpers import (
    files_cleanup,
    get_open_test_img_files,
    close_files,
    get_expected_and_actual,
    get_test_pic_from_file,
)

class CBVTestCase(TestCase):

    ##
    # RESOLVE
    ##

    def test_login_url_should_resolve(self):
        url = '/login/'
        view_class = CumbiaLoginView

        response = self.client.get(url)
        expected, actual = get_expected_and_actual(
            view_class, response
        )

        self.assertEqual(expected, actual)

    def test_logout_url_should_resolve(self):
        url = '/logout/'
        view = cumbia_logout

        response = self.client.get(url)
        actual = response.resolver_match.func

        self.assertEqual(view, actual)

    def test_index_url_should_resolve(self):
        url = '/'
        view_class = IndexView

        response = self.client.get(url)
        expected, actual = get_expected_and_actual(
            view_class, response
        )

        self.assertEqual(expected, actual)

    def test_about_url_should_resolve(self):
        url = '/about/'
        view_class = AboutView

        response = self.client.get(url)
        expected, actual = get_expected_and_actual(
            view_class, response
        )

        self.assertEqual(expected, actual)

    def test_contact_url_should_resolve(self):
        url = '/contact/'
        view_class = ContactView

        response = self.client.get(url)
        expected, actual = get_expected_and_actual(
            view_class, response
        )

        self.assertEqual(expected, actual)

    def test_ph_create_url_should_resolve(self):
        url = '/phs/new/'
        view_class = PhCreateView

        response = self.client.get(url)
        expected, actual = get_expected_and_actual(
            view_class, response
        )

        self.assertEqual(expected, actual)

    def test_ph_create_confirm_url_should_resolve(self):
        ph = Photographer.objects.create(
            first_name='Don',
            last_name='Johnson'
        )
        url = f'/phs/confirm/{ph.pk}/'
        view_class = PhCreateConfirmView

        response = self.client.get(url)
        expected, actual = get_expected_and_actual(
            view_class, response
        )

        self.assertEqual(expected, actual)

    def test_ph_detail_url_should_resolve(self):
        ph = Photographer.objects.create(
            first_name='Silvester',
            last_name='Stallone'
        )
        url = f'/phs/detail/{ph.pk}/'
        view_class = PhDetailView

        response = self.client.get(url)
        expected, actual = get_expected_and_actual(
            view_class, response
        )

        self.assertEqual(expected, actual)

    def test_ph_add_pics_url_should_resolve(self):
        ph = Photographer.objects.create(
            first_name='Chuck',
            last_name='Norris'
        )
        url = f'/phs/add_pics/{ph.pk}/'
        view_class = PhAddPicsView

        response = self.client.get(url)
        expected, actual = get_expected_and_actual(
            view_class, response
        )

        self.assertEqual(expected, actual)

    def test_ph_add_first_pics_url_should_resolve(self):
        ph = Photographer.objects.create(
            first_name='Emiliano',
            last_name='Grillo'
        )
        url = f'/phs/add_first/{ph.pk}/'
        view_class = PhAddFirstPicsView

        response = self.client.get(url)
        expected, actual = get_expected_and_actual(
            view_class, response
        )

        self.assertEqual(expected, actual)

    ##
    # TEMPLATE
    ##

    def test_login_should_render_expected_template(self):
        url = '/login/'
        expected_template = 'portfolio/login.html'
        response = self.client.get(url)
        self.assertTemplateUsed(response, expected_template)

    def test_index_should_render_expected_template(self):
        url = '/'
        expected_template = 'portfolio/index.html'
        response = self.client.get(url)
        self.assertTemplateUsed(response, expected_template)

    def test_about_should_render_expected_template(self):
        url = '/about/'
        expected_template = 'portfolio/about.html'
        response = self.client.get(url)
        self.assertTemplateUsed(response, expected_template)

    def test_contact_should_render_expected_template(self):
        url = '/contact/'
        expected_template = 'portfolio/contact.html'
        response = self.client.get(url)
        self.assertTemplateUsed(response, expected_template)

    def test_ph_create_should_render_expected_template(self):
        url = '/phs/new/'
        expected_template = 'portfolio/ph_create.html'
        response = self.client.get(url)
        self.assertTemplateUsed(response, expected_template)

    def test_ph_create_confirm_should_render_expected_template(self):
        ph = Photographer.objects.create(
            first_name='Mark',
            last_name='Whalberg'
        )
        url = f'/phs/confirm/{ph.pk}/'

        expected_template = 'portfolio/ph_create_confirm.html'

        response = self.client.get(url)

        self.assertTemplateUsed(response, expected_template)

    def test_ph_detail_should_render_expected_template(self):
        ph = Photographer.objects.create(
            first_name='Jean Claude',
            last_name='Van Damme'
        )
        url = f'/phs/detail/{ph.pk}/'

        expected_template = 'portfolio/ph_detail.html'

        response = self.client.get(url)

        self.assertTemplateUsed(response, expected_template)

    def test_ph_add_pics_should_render_expected_template(self):
        ph = Photographer.objects.create(
            first_name='Gene',
            last_name='Hackman'
        )
        url = f'/phs/add_pics/{ph.pk}/'

        expected_template = 'portfolio/ph_add_pics.html'

        response = self.client.get(url)

        self.assertTemplateUsed(response, expected_template)

    def test_ph_add_first_pics_should_render_expected_template(self):
        ph = Photographer.objects.create(
            first_name='Renè',
            last_name='Russo'
        )
        url = f'/phs/add_first/{ph.pk}/'

        expected_template = 'portfolio/ph_add_first_pics.html'

        response = self.client.get(url)

        self.assertTemplateUsed(response, expected_template)

    ##
    # CONTENT
    ##

    def test_login_should_not_display_photographers(self):
        ph_1 = Photographer.objects.create(
            first_name='Dolph',
            last_name='Lundgren'
        )
        ph_2 = Photographer.objects.create(
            first_name='Jet',
            last_name='Li',
        )
        url = '/login/'

        response = self.client.get(url)

        expected_1 = 'Dolph Lundgren'
        expected_2 = 'Jet Li'
        self.assertNotContains(response, expected_1)
        self.assertNotContains(response, expected_2)

    def test_l_col_should_display_photographers(self):
        ph_1 = Photographer.objects.create(
            first_name='Steven',
            last_name='Seagal',
            show=True,
        )
        ph_2 = Photographer.objects.create(
            first_name='Arnold',
            last_name='Schwarzenegger',
            display_name='Arnie',
            show=True,
        )
        url = '/'

        response = self.client.get(url)

        expected_1 = 'Steven Seagal'
        expected_2 = 'Arnie'
        self.assertContains(response, expected_1)
        self.assertContains(response, expected_2)

    def test_l_col_should_contain_photographer_urls(self):
        ph_1 = Photographer.objects.create(
            first_name='Adam',
            last_name='Sandler',
            show=True,
        )
        ph_2 = Photographer.objects.create(
            first_name='Seth',
            last_name='Rogen',
            show=True,
        )
        url = '/'

        response = self.client.get(url)

        link_url_1 = reverse('portfolio:ph_detail', args=[ph_1.pk])
        link_url_2 = reverse('portfolio:ph_detail', args=[ph_2.pk])

        self.assertContains(response, f'<a href="{link_url_1}">')
        self.assertContains(response, f'<a href="{link_url_2}">')

    ##
    # FUNCTION CALLS
    ##

    @patch('portfolio.models.Photographer.control_showable')
    def test_create_confirm_should_call_control_showable(self, mock_control_showable):
        ph = Photographer.objects.create(
            first_name='Adam',
            last_name='Sandler',
            show=True,
        )
        url = f'/phs/confirm/{ph.pk}/'

        response = self.client.get(url)

        self.assertTrue(mock_control_showable.call_count == 1)

class JSONViewsTestCase(TestCase):

    def tearDown(self):
        files_cleanup()

    # RESOLVE

    def test_save_pics_url_should_resolve(self):
        ph = Photographer.objects.create(
            first_name='Don',
            last_name='Johnson'
        )
        url = f'/phs/savepics/{ph.pk}/'
        view_func = save_new_pics

        response = self.client.get(url)

        self.assertEqual(response.resolver_match.func, view_func)

    def test_sort_ph_url_should_resolve(self):
        url = '/phs/sort/'
        view_func = sort_ph

        response = self.client.get(url)

        self.assertEqual(response.resolver_match.func, view_func)

    def test_sort_pic_url_should_resolve(self):
        ph = Photographer.objects.create(
            first_name='Deborah',
            last_name='De Corral'
        )
        url = f'/phs/sortpics/{ph.pk}/'
        view_func = sort_pic

        response = self.client.get(url)

        self.assertEqual(response.resolver_match.func, view_func)

    # BEHAVIOUR

    def test_should_create_pic_objects(self):
        ph = Photographer.objects.create(
            first_name='Jason',
            last_name='Statham'
        )
        url = f'/phs/savepics/{ph.pk}/'
        open_files = get_open_test_img_files()

        response = self.client.post(url, open_files)
        close_files(open_files)

        data = json.loads(response.content.decode())
        pics_created = data['pics_created']
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ph.pics.filter(pk=pics_created[0]).exists())
        self.assertTrue(ph.pics.filter(pk=pics_created[1]).exists())
        self.assertTrue(ph.pics.filter(pk=pics_created[2]).exists())

    def test_should_sort_ph(self):
        ph_1 = Photographer.objects.create(
            first_name='Don',
            last_name='Johnson'
        )
        ph_2 = Photographer.objects.create(
            first_name='Dwayne',
            last_name='Johnson',
            display_name='The Rock'
        )
        ph_3 = Photographer.objects.create(
            first_name='Mark',
            last_name='Whalberg'
        )
        url = '/phs/sort/'

        response = self.client.post(
            url,
            {
                'obj_pk': ph_1.pk,
                'new_idx': 3,
            }
        )

        self.assertTrue(Photographer.objects.get(display_idx=1) == ph_2)
        self.assertTrue(Photographer.objects.get(display_idx=2) == ph_3)
        self.assertTrue(Photographer.objects.get(display_idx=3) == ph_1)

    def test_should_sort_pic(self):
        ph = Photographer.objects.create(
            first_name='Wesley',
            last_name='Snipes'
        )
        pic_1 = get_test_pic_from_file('portrait')
        pic_2 = get_test_pic_from_file('big')
        pic_3 = get_test_pic_from_file('landscape')
        ph.add_pics((pic_1, pic_2, pic_3))
        url = f'/phs/sortpics/{ph.pk}/'

        response = self.client.post(
            url,
            {
                'obj_pk': pic_1.pk,
                'new_idx': 3,
            }
        )

        self.assertTrue(ph.pics.get(display_idx=1) == pic_2)
        self.assertTrue(ph.pics.get(display_idx=2) == pic_3)
        self.assertTrue(ph.pics.get(display_idx=3) == pic_1)
