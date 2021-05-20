import inspect
import os

from PIL import Image

from django.core.files import File
from django.core.files.images import ImageFile
from django.test import (
    TestCase,
)

from portfolio.models import Photographer, Pic
from .helpers import (
    files_cleanup,
    get_test_img_file,
    get_expected_path
)

class PhotographerModelsTest(TestCase):

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

class PicTestCase(TestCase):

    def tearDown(self):
        files_cleanup()

    def test_should_save_and_delete_image(self):
        test_file = get_test_img_file('portrait')
        instance = Pic()

        with open(f'portfolio/tests/{test_file}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            instance.pic = ImageFile(img_file)
            instance.save()

        expected_path = get_expected_path(test_file)
        self.assertEqual(instance.pic.path, expected_path)

        instance.delete()
        deleted_path = expected_path
        self.assertFalse(os.path.exists(deleted_path))

    def test_should_resize_at_save(self):
        test_file = get_test_img_file('landscape')
        instance = Pic()

        with open(f'portfolio/tests/{test_file}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            orig_height, orig_width = img_file.height, img_file.width
            instance.pic = ImageFile(img_file)
            instance.save()

        new_height, new_width = instance.pic.height, instance.pic.width
        self.assertTrue(new_height < orig_height)
        self.assertTrue(new_width < orig_width)
        self.assertTrue(new_height <= 1920)
        self.assertTrue(new_width <= 1920)

    def test_should_keep_ratio_at_resize(self):
        test_file = get_test_img_file('big')
        instance = Pic()

        with open(f'portfolio/tests/{test_file}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            orig_ratio = round(img_file.height / img_file.width, 2)
            instance.pic = ImageFile(img_file)
            instance.save()

        new_ratio = round(instance.pic.height / instance.pic.width, 2)
        self.assertEqual(orig_ratio, new_ratio)

    def test_should_return_photographer_property(self):
        test_file = get_test_img_file('portrait')
        instance = Pic()
        ph = Photographer.objects.create(
            first_name='Ph',
            last_name='For Portarit',
        )

        with open(f'portfolio/tests/{test_file}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            instance.pic = ImageFile(img_file)
            instance.save()
        ph.pics.add(instance)

        self.assertTrue(instance.photographer == ph)
