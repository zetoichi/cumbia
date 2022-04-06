from __future__ import annotations

from typing import List, IO, Type, Sequence

from django.conf import settings
from django.core.exceptions import (
    ImproperlyConfigured,
)
from django.db import models
from django.utils.translation import gettext as _

from . import managers
from core.helpers import resize_img


class SortableModel(models.Model):
    display_idx = models.IntegerField(verbose_name=_("Orden"), default=1)

    def assign_idx(self: SortableModel, idx: int) -> None:
        self.display_idx = idx
        self.save()

    class Meta:
        abstract = True


class Photographer(SortableModel):
    first_name = models.CharField(max_length=100, verbose_name=_("Nombre"))
    last_name = models.CharField(max_length=100, verbose_name=_("Apellido"))
    display_name = models.CharField(
        max_length=100, blank=True, default="", verbose_name=_("Nombre Display")
    )
    bio = models.TextField(blank=True, default="")
    show = models.BooleanField(default=False, verbose_name=_("Mostrar"))
    pics = models.ManyToManyField("Pic", blank=True, verbose_name=_("Fotos"))
    country = models.CharField(
        max_length=100,
        choices=settings.COUNTRIES,
        default="Argentina",
        verbose_name=_("País"),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects = managers.PhotographerManager()

    min_pics = 5

    class Meta:
        verbose_name = _("Photographer")
        verbose_name_plural = _("Photographers")
        ordering = ["display_idx"]

    @property
    def main_pic(self):
        return self.get_main_pic()

    @property
    def red(self):
        return self._has_no_pics()

    @property
    def yellow(self):
        return self._pics_under_min()

    @property
    def green(self):
        return self._pics_over_min()

    def __str__(self):
        return self.display_name

    def save(self: Photographer, *args, **kwargs):
        self._normalize_name()
        if self.display_name == "":
            self.display_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)

    def delete(self: Photographer, *args, **kwargs):
        self.pics.all().delete()
        super().delete(*args, **kwargs)

    def get_absolute_url(self):
        return f"/phs/detail/{self.pk}/"

    def control_showable(self) -> None:
        if self._has_no_pics():
            self.show = False
            self.save()

    def add_pics(self: Photographer, new_pics: Sequence[Pic]) -> None:
        """Wraps m2m add() method"""
        first = self._has_no_pics()

        self.pics.sort_incoming(new_pics)
        self.pics.add(*new_pics)  # perform actual adding
        if first:
            new_pics[0].set_as_main()

    def set_new_main_pic(self: Photographer, pic: Pic) -> None:
        if self._main_pic_belongs_here(pic):
            self.pics.update(main=False)
            pic.main = True
            pic.save()

    def get_main_pic(self) -> Type["Pic"]:
        return self._unique_main_pic()

    def pics_from_files(
        self: Photographer, files: Sequence[IO]
    ) -> List[Type["Pic"]]:
        """Return created objects pk for JSON response."""
        pics_created = []

        for f in files:
            new_pic = Pic.objects.create(
                pic=f,
            )
            pics_created.append(new_pic)
        self.add_pics(pics_created)

        return [pic.pk for pic in pics_created]

    ##
    # PRIVATE METHODS
    ##

    def _has_no_pics(self):
        return self.pics.count() == 0

    def _pics_under_min(self):
        return 0 < self.pics.count() < self.min_pics

    def _pics_over_min(self):
        return self.pics.count() >= self.min_pics

    def _normalize_name(self):
        """Force title format on new objects"""
        self.first_name = self.first_name.title()
        self.last_name = self.last_name.title()

    def _main_pic_belongs_here(self: Photographer, pic: Pic) -> bool:
        if self.pics.filter(pk=pic.pk).exists():
            return True
        raise ImproperlyConfigured(
            """The provided Pic instance does not belong to this Photographer"""
        )

    def _unique_main_pic(self):
        main = self.pics.filter(main=True)
        if main.count() == 1:
            main = main.first()
        elif main.count() == 0:
            main = None
        elif main.count() > 1:
            raise ImproperlyConfigured(
                (
                    """Photographer objects can only have main pic assigned at a time"""
                )
            )
        return main


class Pic(SortableModel):
    pic = models.ImageField(upload_to="pics", verbose_name=_("Image"))
    caption = models.CharField(
        max_length=250, blank=True, default="", verbose_name=_("Caption")
    )
    main = models.BooleanField(
        default=False,
        verbose_name=_("Main"),
    )
    landscape = models.BooleanField(
        default=False,
        verbose_name=_("Main"),
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    objects = managers.PicManager()

    @property
    def photographer(self) -> Type[Photographer] | None:
        if self.photographer_set.count() == 1:  # type: ignore
            return self.photographer_set.first()  # type: ignore
        else:
            return None

    @property
    def is_main(self):
        return self.main is True

    def set_as_main(self: Pic):
        self.main = True
        self.save()

    def set_orientation(self: Pic):
        if self.pic.width > self.pic.height:
            self.landscape = True

    def save(self: Pic, *args, **kwargs):
        self.handle_no_ph()
        self.set_orientation()
        super().save(*args, **kwargs)
        resize_img(self.pic.path)

    def delete(self: Pic, *args, **kwargs):
        self.pic.delete(save=False)
        super().delete(*args, **kwargs)

    def handle_no_ph(self):
        """Pics with no photographer shouldn't be marked as main"""
        if self.main is True and not self.photographer:
            self.main = False

    class Meta:
        verbose_name = _("Foto")
        verbose_name_plural = _("Fotos")
        ordering = ["display_idx"]
