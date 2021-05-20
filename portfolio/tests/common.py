import os

from django.conf import settings

UPLOADED_PICS_PATH = os.path.join(settings.MEDIA_ROOT, 'pics')
TEST_IMAGE_FILES = {
    'portrait': 'ozFsMoAW_testpic_portrait.jpg',
    'landscape': 'BreHayL8_testpic_landscape.jpg',
    'big': '4wmdrys5_testpic_big.jpg',
}

def files_cleanup():
    for filename in TEST_IMAGE_FILES.values():
        path = os.path.join(UPLOADED_PICS_PATH, filename)
        if os.path.exists(path):
            os.remove(path)
