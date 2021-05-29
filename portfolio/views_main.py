from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from .signals import see_this
from .mixins import GeneralContextMixin
from .models import (
    Photographer,
    Pic,
)

class IndexView(GeneralContextMixin, TemplateView):
    template_name = 'portfolio/index.html'

class AboutView(GeneralContextMixin, TemplateView):
    template_name = 'portfolio/about.html'

class PhDetailView(GeneralContextMixin, DetailView):
    template_name = 'portfolio/ph_detail.html'
    model = Photographer
    context_object_name = 'ph'

class PhAddPicsView(GeneralContextMixin, DetailView):
    template_name = 'portfolio/ph_add_pics.html'
    model = Photographer
    context_object_name = 'ph'
