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
    display_idx = models.IntegerField(
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

    def _sort_pics(self, pics: Sequence[Type['Pic']], start: int = 0) -> None:
        [pic.assign_idx(start + i) for i, pic in enumerate(pics, 1)]

    def _insort_right(self, pic: Type['Pic'], new_idx: int) -> None:
        """
        Move pic up, shift rest of set right.
        """
        start = new_idx
        self._sort_pics(self.pics.filter(display_idx__gte=new_idx), start)
        pic.assign_idx(new_idx)

    def _insort_left(self, pic: Type['Pic'], new_idx: int) -> None:
        """
        Move pic down, shift rest of set left.
        """
        self._sort_pics(self.pics.filter(display_idx__lte=new_idx)[1:])
        pic.assign_idx(new_idx)

    def _sort_incoming(self, pics: Sequence[Type['Pic']]) -> None:
        """
        Assign display order to new pics,
        starting from last element in self.pics
        """
        start = self.pics.count()
        self._sort_pics(pics, start)

    def add_pics(self, pics: Sequence[Type['Pic']]) -> None:
        """
        Wraps m2m add() method to:
            - Sort incoming pics
            - Check if the added object is the first in the set,
            - Mark it as main if it is.
        """
        first = self._has_no_pics()
        self._sort_incoming(pics)
        self.pics.add(*pics)  # perform actual adding
        if first:
            pics[0].set_as_main()

    def set_new_main_pic(self, pic: Type['Pic']) -> None:
        if self._main_pic_belongs_here(pic):
            self.pics.update(main=False)
            pic.main = True
            pic.save()

    def get_main_pic(self) -> Type['Pic']:
        return self._unique_main_pic()

    def insort_pic(self, pic: Type['Pic'], new_idx: int) -> None:
        old_idx = pic.display_idx
        if new_idx < old_idx:
            self._insort_right(pic, new_idx)
        elif new_idx > old_idx:
            self._insort_left(pic, new_idx)

    def pics_from_files(self, files: Sequence[IO]) -> List[Type['Pic']]:
        """
        Create Pic objects for the related Field pics.
        Return created objects pk for JSON response.
        """
        pics_created = []

        for f in files:
            new_pic = Pic.objects.create(
                pic=f,
                caption=lorem.words(6)  # TEMPORARY LOREM FOR CAPTION, DELETE
            )
            pics_created.append(new_pic)
        self.add_pics(pics_created)

        return [pic.pk for pic in pics_created]

    def save(self, *args, **kwargs):
        self._normalize_name()
        if self.display_name == '':
            self.display_name = f'{self.first_name} {self.last_name}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name

    class Meta:
        verbose_name = _('Photographer')
        verbose_name_plural = _('Photographers')
        ordering = ['display_idx']


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
    display_idx = models.IntegerField(
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

    def assign_idx(self, idx: int) -> None:
        self.display_idx = idx
        self.save()

    def set_as_main(self):
        self.main = True
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        """For resize image"""
        resize_img(self.pic.path)
        self.handle_no_ph()

    def delete(self, *args, **kwargs):
        """Delete file upon object deletion"""
        self.pic.delete(save=False)
        super().delete(*args, **kwargs)

    def handle_no_ph(self):
        """Pics with no photographer can't be marked as main"""
        if self.main is True and not self.photographer:
            self.main = False

    class Meta:
        verbose_name = _('Foto')
        verbose_name_plural = _('Fotos')
        ordering = ['display_idx']
