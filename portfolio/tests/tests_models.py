import inspect
import os
import time

from PIL import Image

from django.core.exceptions import ImproperlyConfigured
from django.core.files import File
from django.core.files.images import ImageFile
from django.test import (
    TestCase,
)

from portfolio.models import Photographer, Pic
from .helpers import (
    files_cleanup,
    get_test_img_file,
    get_test_pic_from_file,
    get_expected_path,
)

class PhotographerModelsTest(TestCase):

    def tearDown(self):
        files_cleanup()

    # INSTANCE METHODS

    def test_should_build_display_name(self):
        ph = Photographer.objects.create(
            first_name='First',
            last_name='Fake Ph'
        )
        get_ph = Photographer.objects.get(pk=ph.pk)
        self.assertEqual(get_ph.display_name, 'First Fake Ph')

    def test_should_use_given_display_name(self):
        ph = Photographer.objects.create(
            first_name='Second',
            last_name='Fake Ph',
            display_name='Display'
        )
        get_ph = Photographer.objects.get(pk=ph.pk)
        self.assertEqual(ph.display_name, 'Display')

    def test_should_normalize_name(self):
        ph = Photographer.objects.create(
            first_name='fIRST',
            last_name='fAke pH'
        )
        self.assertEqual(ph.first_name, 'First')
        self.assertEqual(ph.last_name, 'Fake Ph')

    # INSTANCE METHODS THAT HANDLE PICS SET

    def test_set_new_main_pic_should_raise_improperly_configured(self):
        ph = Photographer.objects.create(
            first_name='Gloria',
            last_name='Gaynor'
        )
        pic = get_test_pic_from_file('portrait')

        self.assertRaises(ImproperlyConfigured, lambda: ph.set_new_main_pic(pic))

    def test_get_new_main_pic_should_raise_improperly_configured(self):
        ph = Photographer.objects.create(
            first_name='Gloria',
            last_name='Gaynor'
        )

        self.assertRaises(ImproperlyConfigured, lambda: ph.get_main_pic())

    def test_should_set_new_main_pic(self):
        ph = Photographer.objects.create(
            first_name='Ennio',
            last_name='Morricone'
        )
        pic = get_test_pic_from_file('portrait')
        ph.add_pics((pic,))

        ph.set_new_main_pic(pic)

        self.assertTrue(pic.main)

    def test_set_new_main_pic_should_be_unique(self):
        ph = Photographer.objects.create(
            first_name='Ennio',
            last_name='Morricone'
        )
        pic_1 = get_test_pic_from_file('portrait')
        pic_2 = get_test_pic_from_file('big')
        ph.add_pics((pic_1, pic_2))

        self.assertTrue(ph.main_pic == pic_1)

        ph.set_new_main_pic(pic_2)

        self.assertFalse(ph.main_pic == pic_1)
        self.assertTrue(ph.main_pic == pic_2)

    def test_first_pic_should_add_pics_and_mark_as_main(self):
        ph = Photographer.objects.create(
            first_name='New',
            last_name='Ph',
        )
        pic = get_test_pic_from_file('portrait')
        ph.add_pics((pic,))

        self.assertTrue(pic.is_main)

    def test_should_add_pics_and_sort(self):
        ph = Photographer.objects.create(
            first_name='New',
            last_name='Ph',
        )
        pic_1 = get_test_pic_from_file('portrait')
        pic_2 = get_test_pic_from_file('big')
        pic_3 = get_test_pic_from_file('landscape')
        ph.add_pics((pic_1, pic_2, pic_3))

        self.assertTrue(ph.pics.count() == 3)
        self.assertTrue(pic_1.display_order == 1)
        self.assertTrue(pic_2.display_order == 2)
        self.assertTrue(pic_3.display_order == 3)

class PicTestCase(TestCase):

    def tearDown(self):
        files_cleanup()

    def test_should_save_and_delete_image(self):
        test_file = get_test_img_file('portrait')
        pic = Pic()

        with open(f'portfolio/tests/{test_file}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            pic.pic = ImageFile(img_file)
            pic.save()

        expected_path = get_expected_path(test_file)
        self.assertEqual(pic.pic.path, expected_path)

        pic.delete()
        deleted_path = expected_path
        self.assertFalse(os.path.exists(deleted_path))

    def test_should_resize_at_save(self):
        test_file = get_test_img_file('landscape')
        pic = Pic()

        with open(f'portfolio/tests/{test_file}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            orig_height, orig_width = img_file.height, img_file.width
            pic.pic = ImageFile(img_file)
            pic.save()

        new_height, new_width = pic.pic.height, pic.pic.width
        self.assertTrue(new_height < orig_height)
        self.assertTrue(new_width < orig_width)
        self.assertTrue(new_height <= 1920)
        self.assertTrue(new_width <= 1920)

    def test_should_keep_ratio_at_resize(self):
        test_file = get_test_img_file('big')
        pic = Pic()

        with open(f'portfolio/tests/{test_file}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            orig_ratio = round(img_file.height / img_file.width, 2)
            pic.pic = ImageFile(img_file)
            pic.save()

        new_ratio = round(pic.pic.height / pic.pic.width, 2)
        self.assertEqual(orig_ratio, new_ratio)

    def test_photographer_property_should_return_ph(self):
        test_file = get_test_img_file('portrait')
        pic = Pic()
        ph = Photographer.objects.create(
            first_name='Ph',
            last_name='For Portarit',
        )

        with open(f'portfolio/tests/{test_file}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            pic.pic = ImageFile(img_file)
            pic.save()
        ph.add_pics((pic,))

        self.assertTrue(pic.photographer == ph)

    def test_photographer_property_should_return_none(self):
        test_file = get_test_img_file('portrait')
        pic = Pic()

        with open(f'portfolio/tests/{test_file}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            pic.pic = ImageFile(img_file)
            pic.save()

        self.assertTrue(pic.photographer is None)

    def test_should_not_get_marked_as_main(self):
        test_file = get_test_img_file('portrait')
        pic = Pic()

        with open(f'portfolio/tests/{test_file}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            pic.pic = ImageFile(img_file)
            pic.main = True
            pic.save()

        self.assertFalse(pic.is_main)
