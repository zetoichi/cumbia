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

class SortableModel(models.Model):
    display_idx = models.IntegerField(
        verbose_name=_('Orden'),
        default=1
    )

    def assign_idx(self, idx: int) -> None:
        self.display_idx = idx
        self.save()

    class Meta:
        abstract = True

class Photographer(SortableModel):
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

    def save(self, *args, **kwargs):
        self._normalize_name()
        if self.display_name == '':
            self.display_name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f'/phs/detail/{self.pk}/'

    def _normalize_name(self):
        """Force title format on new objects"""
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()

    def _main_pic_belongs_here(self, pic: Type['Pic']) -> bool:
        if self.pics.filter(pk=pic.pk).exists():
            return True
        raise ImproperlyConfigured(
            """The provided Pic instance does not
            belong to this photographer"""
        )

    def _unique_main_pic(self):
        main = self.pics.filter(main=True)
        if main.count() != 1:
            raise ImproperlyConfigured((
                """Photographer objects should have one and
                only main pic assigned at a time"""
            ))
        return main.first()

    def _has_no_pics(self):
        return self.pics.count() == 0

    def _moving_up(self, new_idx: int, old_idx: int) -> bool:
        """Determine sorting strategy"""
        return new_idx < old_idx

    def add_pics(self, new_pics: Sequence[Type['Pic']]) -> None:
        """Wraps m2m add() method"""
        first = self._has_no_pics()

        self.pics.sort_incoming(new_pics)
        self.pics.add(*new_pics)  # perform actual adding
        if first:
            new_pics[0].set_as_main()

    def set_new_main_pic(self, pic: Type['Pic']) -> None:
        if self._main_pic_belongs_here(pic):
            self.pics.update(main=False)
            pic.main = True
            pic.save()

    def get_main_pic(self) -> Type['Pic']:
        return self._unique_main_pic()

    def insort_pic(self, pic: Type['Pic'], new_idx: int) -> None:
        old_idx = pic.display_idx

        if new_idx != old_idx:
            if self._moving_up(new_idx, old_idx):
                self.pics.insort_right(pic, new_idx)
            else:
                self.pics.insort_left(pic, new_idx)

    def pics_from_files(self, files: Sequence[IO]) -> List[Type['Pic']]:
        """Return created objects pk for JSON response."""
        pics_created = []

        for f in files:
            new_pic = Pic.objects.create(
                pic=f,
                caption=lorem.words(6)  # TEMPORARY LOREM FOR CAPTION, DELETE
            )
            pics_created.append(new_pic)
        self.add_pics(pics_created)

        return [pic.pk for pic in pics_created]

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = _('Photographer')
        verbose_name_plural = _('Photographers')
        ordering = ['display_idx']


class Pic(SortableModel):
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

    def handle_no_ph(self):
        """Pics with no photographer shouldn't be marked as main"""
        if self.main is True and not self.photographer:
            self.main = False

    class Meta:
        verbose_name = _('Foto')
        verbose_name_plural = _('Fotos')
        ordering = ['display_idx']
