from typing import Any, Dict, List
from datetime import date

from django.db import models
from pydantic import BaseModel

class Photographer(models.Model):
    name = models.CharField(max_length=250, default='')

class Photo(models.Model):
    photographer = models.ForeignKey(Photographer, on_delete=models.CASCADE, default=None)
    url = models.CharField(max_length=250, default='')