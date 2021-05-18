from django.views.generic.base import TemplateView

from .models import (
    Photographer,
    Pic,
)

class PublicIndexView(TemplateView):
    template_name = 'portfolio/public_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photographers'] = Photographer.objects.all()
        return context
