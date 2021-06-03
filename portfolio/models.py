import time

from typing import Any, Dict, List, IO, Type, Sequence
from datetime import date

from lorem_text import lorem

from django.core.exceptions import (
    MultipleObjectsReturned,
    ImproperlyConfigured,
)
from django.db import models
from django.utils.translation import gettext as _
from pydantic import BaseModel

from . import managers
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
    pics = models.ManyToManyField(
        'Pic',
        blank=True,
        verbose_name=_('Fotos')
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    objects = managers.PhotographerManager()

    @property
    def main_pic(self):
        return self.get_main_pic()

    def normalize_name(self):
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()

    def pics_from_files(self, files: Sequence[IO]) -> List[Type['Pic']]:
        pics_created = []

        for f in files:
            new_pic = Pic.objects.create(
                pic=f,
                caption=lorem.words(6)
            )
            pics_created.append(new_pic)
        self.add_pics(pics_created)

        return [pic.pk for pic in pics_created]

    def add_pics(self, pics: Sequence[Type['Pic']]) -> None:
        first = self.pics.count() == 0
        self.pics.add(*pics)
        if first:
            pics[0].set_as_main()

    def set_new_main_pic(self, pic: Type['Pic']) -> None:
        if self.pics.filter(pk=pic.pk).exists():
            self.pics.update(main=False)
            pic.main = True
            pic.save()
        else:
            raise ImproperlyConfigured(
                """The provided Pic instance does not
                belong to this photographer"""
            )

    def get_main_pic(self) -> Type['Pic']:
        main = self.pics.filter(main=True)
        main_count = main.count()
        if main_count > 1:
            raise ImproperlyConfigured((
                """Photographer objects should have one and
                only main pic assigned at a time"""
            ))
        elif main_count == 0:
            return None
        else:
            return main.first()

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
    caption = models.CharField(
        max_length=250,
        blank=True,
        default='',
        verbose_name=_('Caption')
    )
    main = models.BooleanField(
        default=False,
        verbose_name=_('Main'),
    )
    display_order = models.IntegerField(
        verbose_name=_('Orden'),
        default=1
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    objects = managers.PicManager()

    @property
    def photographer(self) -> Type[Photographer]:
        if self.photographer_set.count() == 1:
            return self.photographer_set.first()
        else:
            return None

    @property
    def is_main(self):
        return self.main is True

    def set_as_main(self):
        self.main = True
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        resize_img(self.pic.path)
        self.handle_no_ph()

    def delete(self, *args, **kwargs):
        self.pic.delete(save=False)
        super().delete(*args, **kwargs)

    # Pics with no photographer can't be marked as main
    def handle_no_ph(self):
        if self.main is True and not self.photographer:
            self.main = False

    class Meta:
        verbose_name = _('Foto')
        verbose_name_plural = _('Fotos')
        ordering = ['display_order']
