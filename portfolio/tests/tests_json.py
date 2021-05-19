import os
from unittest.mock import patch

from django.core.files import File
from django.test import TestCase

from portfolio.views_json import (
    save_new_pics
)
