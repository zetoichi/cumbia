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

    @classmethod
    def setUpTestData(cls):
        cls.ph_1 = Photographer.objects.create(
            first_name='Dolph',
            last_name='Lundgren',
            display_name='Dolphie'
        )
        cls.ph_2 = Photographer.objects.create(
            first_name='Jet',
            last_name='Li',
        )

    def tearDown(self):
        files_cleanup()

    # INSTANCE METHODS

    def test_should_use_given_display_name(self):
        get_ph = Photographer.objects.get(pk=self.ph_1.pk)
        self.assertEqual(get_ph.display_name, 'Dolphie')

    def test_should_build_display_name(self):
        get_ph = Photographer.objects.get(pk=self.ph_2.pk)
        self.assertEqual(get_ph.display_name, 'Jet Li')

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

    def test_should_delete_pics_as_well(self):
        ph = Photographer.objects.create(
            first_name='Tom',
            last_name='Berenger'
        )
        pic = get_test_pic_from_file('portrait')
        ph.add_pics((pic,))

        ph.delete()

        self.assertFalse(Pic.objects.filter(pk=pic.pk).exists())

    def test_set_new_main_pic_not_in_pics_should_raise_improperly_configured(self):
        pic = get_test_pic_from_file('portrait')

        self.assertRaises(ImproperlyConfigured, lambda: self.ph_1.set_new_main_pic(pic))

    def test_get_new_main_pic_should_return_none(self):
        expected = None
        actual = self.ph_1.get_main_pic()

        self.assertEqual(expected, actual)

    def test_should_set_new_main_pic(self):
        pic = get_test_pic_from_file('portrait')
        self.ph_2.add_pics((pic,))

        self.ph_2.set_new_main_pic(pic)

        self.assertTrue(pic.main)

    def test_set_new_main_pic_should_be_unique(self):
        pic_1 = get_test_pic_from_file('portrait')
        pic_2 = get_test_pic_from_file('big')
        self.ph_1.add_pics((pic_1, pic_2))

        self.assertTrue(self.ph_1.main_pic == pic_1)

        self.ph_1.set_new_main_pic(pic_2)

        self.assertFalse(self.ph_1.main_pic == pic_1)
        self.assertTrue(self.ph_1.main_pic == pic_2)

    def test_first_pic_should_add_first_pic_and_mark_as_main(self):
        pic = get_test_pic_from_file('portrait')
        self.ph_1.add_pics((pic,))

        self.assertTrue(pic.is_main)

    def test_should_add_pics_and_sort(self):
        pic_1 = get_test_pic_from_file('portrait')
        pic_2 = get_test_pic_from_file('big')
        pic_3 = get_test_pic_from_file('landscape')
        self.ph_2.add_pics((pic_1, pic_2, pic_3))

        self.assertTrue(self.ph_2.pics.count() == 3)
        self.assertTrue(pic_1.display_idx == 1)
        self.assertTrue(pic_2.display_idx == 2)
        self.assertTrue(pic_3.display_idx == 3)

    def test_should_insort_pic_right(self):
        pic_1 = get_test_pic_from_file('portrait')
        pic_2 = get_test_pic_from_file('big')
        pic_3 = get_test_pic_from_file('landscape')
        self.ph_2.add_pics((pic_1, pic_2, pic_3))

        self.ph_2.pics.insort(pic_3, 1)

        self.assertTrue(self.ph_2.pics.get(display_idx=1) == pic_3)
        self.assertTrue(self.ph_2.pics.get(display_idx=2) == pic_1)
        self.assertTrue(self.ph_2.pics.get(display_idx=3) == pic_2)

    def test_should_insort_pic_left(self):
        pic_1 = get_test_pic_from_file('portrait')
        pic_2 = get_test_pic_from_file('big')
        pic_3 = get_test_pic_from_file('landscape')
        self.ph_1.add_pics((pic_1, pic_2, pic_3))

        self.ph_1.pics.insort(pic_1, 3)

        self.assertTrue(self.ph_1.pics.get(display_idx=1) == pic_2)
        self.assertTrue(self.ph_1.pics.get(display_idx=2) == pic_3)
        self.assertTrue(self.ph_1.pics.get(display_idx=3) == pic_1)

    def test_should_not_be_showable(self):
        self.ph_1.control_showable()

        self.assertFalse(self.ph_1.show)

    def test_no_pics_should_only_be_red(self):
        self.assertTrue(self.ph_1.red)
        self.assertFalse(self.ph_1.yellow)
        self.assertFalse(self.ph_1.green)

    def test_too_few_pics_should_only_be_yellow(self):
        pic_1 = get_test_pic_from_file('portrait')
        pic_2 = get_test_pic_from_file('big')
        pic_3 = get_test_pic_from_file('landscape')
        self.ph_2.add_pics((pic_1, pic_2, pic_3))

        self.assertFalse(self.ph_2.red)
        self.assertTrue(self.ph_2.yellow)
        self.assertFalse(self.ph_2.green)

    def test_should_only_be_green(self):
        pic_1 = get_test_pic_from_file('portrait')
        pic_2 = get_test_pic_from_file('big')
        pic_3 = get_test_pic_from_file('landscape')
        pic_4 = get_test_pic_from_file('big')
        pic_5 = get_test_pic_from_file('landscape')
        self.ph_1.add_pics((pic_1, pic_2, pic_3, pic_4, pic_5))

        self.assertFalse(self.ph_1.red)
        self.assertFalse(self.ph_1.yellow)
        self.assertTrue(self.ph_1.green)

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
