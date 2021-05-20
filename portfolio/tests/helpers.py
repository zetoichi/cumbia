import os
from typing import Tuple, List, Dict, IO, Type

from django.conf import settings
from django.http import HttpResponse

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

def get_test_img_file(img_type: str) -> str:
    return TEST_IMAGE_FILES[img_type]

def get_open_test_img_files() -> Dict[str, IO]:
    open_files = {}
    for i, (_, filename) in enumerate(TEST_IMAGE_FILES.items()):
        f = open(f'portfolio/tests/{filename}', 'rb')
        open_files[f'pic[{i}]'] = f

    return open_files

def close_files(open_files):
    for f in open_files.values():
        f.close()

def get_expected_path(filename):
    return os.path.join(UPLOADED_PICS_PATH, f'{filename}')

def get_expected_and_actual(view_class: Type, response: HttpResponse) -> Tuple[str, str]:
    return (
        view_class.as_view().__name__,
        response.resolver_match.func.__name__
    )
