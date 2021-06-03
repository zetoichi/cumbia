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

    def test_should_sort_new_phs(self):
        phs_count = Photographer.objects.count()
        ph_1 = Photographer.objects.create(
            first_name='Thrid',
            last_name='Fake Ph'
        )
        ph_2 = Photographer.objects.create(
            first_name='Fourth',
            last_name='Fake Ph'
        )
        self.assertEqual(phs_count + 1, ph_1.display_idx)
        self.assertEqual(phs_count + 2, ph_2.display_idx)

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
            first_name='Danny',
            last_name='Elfman',
        )
        pic = get_test_pic_from_file('portrait')
        ph.add_pics((pic,))

        self.assertTrue(pic.is_main)

    def test_should_add_pics_and_sort(self):
        ph = Photographer.objects.create(
            first_name='John',
            last_name='Williams',
        )
        pic_1 = get_test_pic_from_file('portrait')
        pic_2 = get_test_pic_from_file('big')
        pic_3 = get_test_pic_from_file('landscape')
        ph.add_pics((pic_1, pic_2, pic_3))

        self.assertTrue(ph.pics.count() == 3)
        self.assertTrue(pic_1.display_idx == 1)
        self.assertTrue(pic_2.display_idx == 2)
        self.assertTrue(pic_3.display_idx == 3)

    def test_should_insort_pic_right(self):
        ph = Photographer.objects.create(
            first_name='Anne',
            last_name='Dudley',
        )
        pic_1 = get_test_pic_from_file('portrait')
        pic_2 = get_test_pic_from_file('big')
        pic_3 = get_test_pic_from_file('landscape')
        ph.add_pics((pic_1, pic_2, pic_3))

        ph.insort_pic(pic_3, 1)

        self.assertTrue(ph.pics.get(display_idx=1) == pic_3)
        self.assertTrue(ph.pics.get(display_idx=2) == pic_1)
        self.assertTrue(ph.pics.get(display_idx=3) == pic_2)

    def test_should_insort_pic_left(self):
        ph = Photographer.objects.create(
            first_name='Anne',
            last_name='Dudley',
        )
        pic_1 = get_test_pic_from_file('portrait')
        pic_2 = get_test_pic_from_file('big')
        pic_3 = get_test_pic_from_file('landscape')
        ph.add_pics((pic_1, pic_2, pic_3))

        ph.insort_pic(pic_1, 3)

        self.assertTrue(ph.pics.get(display_idx=1) == pic_2)
        self.assertTrue(ph.pics.get(display_idx=2) == pic_3)
        self.assertTrue(ph.pics.get(display_idx=3) == pic_1)

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
        ph = Photographer.objects.create(
            first_name='Ph',
            last_name='For Portarit',
        )
        pic = get_test_pic_from_file('portrait')
        ph.add_pics((pic,))

        self.assertTrue(pic.photographer == ph)

    def test_photographer_property_should_return_none(self):
        pic = get_test_pic_from_file('portrait')

        self.assertTrue(pic.photographer is None)

    def test_should_not_get_marked_as_main(self):
        pic = get_test_pic_from_file('portrait')
        pic.main = True
        pic.save()

        self.assertFalse(pic.is_main)

    def test_should_sort_new_pics(self):
        pic_count = Pic.objects.count()
        test_file_1 = get_test_img_file('landscape')
        test_file_2 = get_test_img_file('portrait')

        with open(f'portfolio/tests/{test_file_1}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            pic_1 = Pic.objects.create(
                pic=ImageFile(img_file)
            )
        with open(f'portfolio/tests/{test_file_2}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            pic_2 = Pic.objects.create(
                pic=ImageFile(img_file)
            )

        self.assertEqual(pic_count + 1, pic_1.display_idx)
        self.assertEqual(pic_count + 2, pic_2.display_idx)
