from typing import Any, Dict, List
from datetime import date

from django.db import models
from django.utils.translation import gettext as _
from pydantic import BaseModel

from core.helpers import resize_img

class Photographer(models.Model):
    first_name = models.CharField(
        max_length=100,
        verbose_name=_('Nombre')
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name=_('Apellido')
    )
    display_name = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name=_('Nombre Display')
    )
    bio = models.TextField(
        blank=True,
        default=''
    )
    display_order = models.IntegerField(
        verbose_name=_('Orden'),
        default=1
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def normalize_name(self):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()

    def save(self, *args, **kwargs):
        self.normalize_name()
        if self.display_name == '':
            self.display_name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = _('Photographer')
        verbose_name_plural = _('Photographers')
        ordering = ['display_order']


class Pic(models.Model):
    pic = models.ImageField(
        upload_to='pics',
        verbose_name=_('Image')
    )
    photographer = models.ForeignKey(
        Photographer,
        on_delete=models.CASCADE,
        related_name='pics'
    )
    caption = models.CharField(
        max_length=250,
        blank=True,
        default='',
        verbose_name=_('Caption')
    )
    display_order = models.IntegerField(
        verbose_name=_('Orden'),
        default=1
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        resize_img(self.pic.path)

    def delete(self, *args, **kwargs):
        self.pic.delete(save=False)
        super().delete(*args, **kwargs)

    def __str__(self):
        if self.title != '':
            string = self.title
        else:
            string = self.pic.name
        return string

    class Meta:
        verbose_name = _('Foto')
        verbose_name_plural = _('Fotos')
        ordering = ['display_order']
