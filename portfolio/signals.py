from django.core.signals import request_finished
from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from core.helpers import get_first_from_pk_set
from .models import (
    Photographer,
    Pic,
)

@receiver(request_finished)
def see_this(sender, **kwargs):
    pass
