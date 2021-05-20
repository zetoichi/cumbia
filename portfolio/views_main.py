from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from .mixins import GeneralContextMixin
from .models import (
    Photographer,
    Pic,
)

class IndexView(GeneralContextMixin, TemplateView):
    template_name = 'portfolio/index.html'

class PhDetailView(GeneralContextMixin, DetailView):
    template_name = 'portfolio/ph_detail.html'
    model = Photographer
    context_object_name = 'ph'
