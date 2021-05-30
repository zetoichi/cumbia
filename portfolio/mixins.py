from django.core.exceptions import ImproperlyConfigured

from .models import (
    Photographer,
    Pic,
)

class GeneralContextMixin:

    segment = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photographers'] = Photographer.objects.all()
        context['segment'] = self.get_segment()
        return context

    def get_segment(self):
        if self.segment is not None:
            return self.segment
        else:
            raise ImproperlyConfigured(
                'GeneralContextMixin requires a value for the "segment" attribute'
            )
