import inspect
import os

from PIL import Image

from django.core.files import File
from django.core.files.images import ImageFile
from django.test import (
    TestCase,
)
from django.conf import settings

from portfolio.models import Photographer, Pic

UPLOADED_PICS_PATH = os.path.join(settings.MEDIA_ROOT, 'pics')

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

    test_image_files = [
        'ozFsMoAW_testpic_portrait.jpg',
        'BreHayL8_testpic_landscape.jpg',
        '4wmdrys5_testpic_big.jpg',
    ]

    def tearDown(self):
        for filename in self.test_image_files:
            path = os.path.join(UPLOADED_PICS_PATH, filename)
            if os.path.exists(path):
                os.remove(path)

    def test_should_save_and_delete_image(self):
        test_file = self.test_image_files[0]
        instance = Pic()
        pk = instance.pk
        ph = Photographer.objects.create(
            first_name='Ph',
            last_name='With Pic',
        )
        instance.photographer = ph

        with open(f'portfolio/tests/{test_file}', 'rb') as img_file:
            img_file = ImageFile(img_file)
            img_file.name = img_file.name.split('/')[-1]
            instance.pic = ImageFile(img_file)
            instance.save()

        expected_path = os.path.join(UPLOADED_PICS_PATH, f'{test_file}')
        self.assertEqual(instance.pic.path, expected_path)

        instance.delete()
        deleted_path = expected_path
        self.assertFalse(Pic.objects.filter(pk=pk).exists())
        self.assertFalse(os.path.exists(deleted_path))
