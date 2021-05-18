from .models import (
    Photographer,
    Pic,
)

class GeneralContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photographers'] = Photographer.objects.all()
        return context
