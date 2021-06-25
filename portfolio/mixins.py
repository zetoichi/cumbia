from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User

from .models import (
    Photographer,
    Pic,
)
from .forms import PhotographerForm, UserCreateForm

class GeneralContextMixin:

    segment: str = None
    sub_segment: str = None
    creating: bool = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_is_auth = self.request.user.is_authenticated
        context['edit_mode'] = user_is_auth
        context['photographers'] = Photographer.objects.visible_for(user_is_auth)
        context['segment'] = self.get_segment()
        context['sub_segment'] = self.sub_segment if self.sub_segment is not None else None
        context['creating'] = self.get_creating()
        context['get_back'] = self.request.META.get('HTTP_REFERER')
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
            self.request.session['creating'] = self.creating
            return self.creating
        else:
            raise ImproperlyConfigured(
                'GeneralContextMixin requires a value for the "creating" attribute'
            )

class UserDetailMixin:
    model = User
    form_class = UserCreateForm
    context_object_name = 'usr'

class PhDetailMixin:
    model = Photographer
    form_class = PhotographerForm
    context_object_name = 'ph'

class GalleryMixin:
    gallery = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = self.get_gallery()
        return context

    def get_gallery(self):
        if self.gallery is not None:
            return self.gallery
        else:
            raise ImproperlyConfigured(
                'GalleryMixin requires a value for the "gallery" attribute'
            )
