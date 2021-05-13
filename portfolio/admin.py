from django.contrib import admin
from .models import (
    Photographer,
    Pic,
)

admin.site.register(Photographer)
admin.site.register(Pic)
