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
    segment = 'index'

class AboutView(GeneralContextMixin, TemplateView):
    template_name = 'portfolio/about.html'
    segment = 'info'

class ContactView(GeneralContextMixin, TemplateView):
    template_name = 'portfolio/contact.html'
    segment = 'info'

class PhDetailView(GeneralContextMixin, DetailView):
    template_name = 'portfolio/ph_detail.html'
    model = Photographer
    context_object_name = 'ph'
    segment = 'detail'

class PhDetailAltView(GeneralContextMixin, DetailView):
    template_name = 'portfolio/ph_detail_alt.html'
    model = Photographer
    context_object_name = 'ph'
    segment = 'detail'

class PhAddPicsView(GeneralContextMixin, DetailView):
    template_name = 'portfolio/ph_add_pics.html'
    model = Photographer
    context_object_name = 'ph'
    segment = 'detail'
