# from typing import Type

from django.db.models import Model
from django.conf import settings

import shortuuid
from PIL import Image

# IMAGE HELPERS
#

def generate_uuid(length: int = 22) -> str:
    """Generate a UUID"""
    return shortuuid.ShortUUID().random(length=length)

def resize_img(image_path: str) -> None:
    target_size = settings.MAX_IMAGE_SIZE
    img = Image.open(image_path)

    if img.width > target_size[0] or img.height > target_size[1]:
        img.thumbnail(target_size)
        img.save(image_path)
