from django.core.exceptions import ImproperlyConfigured

from .models import (
    Photographer,
    Pic,
)

class GeneralContextMixin:

    segment: str = None
    creating: bool = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_is_auth = self.request.user.is_authenticated
        context['edit_mode'] = user_is_auth
        context['photographers'] = Photographer.objects.visible_for(user_is_auth)
        context['segment'] = self.get_segment()
        context['creating'] = self.get_creating()
        print('############### ', context['creating'])
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
