from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User

from .models import (
    Photographer,
)
from .forms import PhotographerForm, UserCreateForm
from .utils import get_user_country


class GeneralContextMixin:

    segment: str = None
    sub_segment: str = None
    creating: bool = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_is_auth = self.request.user.is_authenticated
        user_country = get_user_country(self.request)

        context["edit_mode"] = user_is_auth
        context["user_country"] = user_country
        print("################", user_country)
        context["from_arg"] = Photographer.objects.from_arg(user_is_auth)
        context["from_chile"] = Photographer.objects.from_chile(user_is_auth)
        context["segment"] = self.get_segment()
        context["sub_segment"] = (
            self.sub_segment if self.sub_segment is not None else None
        )
        context["creating"] = self.get_creating()
        context["get_back"] = self.request.META.get("HTTP_REFERER")
        context["show_intro"] = self.get_show_intro()
        return context

    def get_segment(self):
        if self.segment is not None:
            return self.segment
        else:
            raise ImproperlyConfigured(
                'GeneralContextMixin requires a value for the "segment" attribute'
            )

    def get_creating(self):
        if self.creating is not None:
            self.request.session["creating"] = self.creating
            return self.creating
        else:
            raise ImproperlyConfigured(
                'GeneralContextMixin requires a value for the "creating" attribute'
            )

    def get_show_intro(self):
        show = True
        if self.request.session.get("show_intro") == 0:
            show = False
        else:
            self.request.session["show_intro"] = 0
            self.request.session.set_expiry(1800)
        return show


class UserDetailMixin:
    model = User
    form_class = UserCreateForm
    context_object_name = "usr"


class PhDetailMixin:
    model = Photographer
    form_class = PhotographerForm
    context_object_name = "ph"


class GalleryMixin:
    gallery = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["gallery"] = self.get_gallery()
        return context

    def get_gallery(self):
        if self.gallery is not None:
            return self.gallery
        else:
            raise ImproperlyConfigured(
                'GalleryMixin requires a value for the "gallery" attribute'
            )
