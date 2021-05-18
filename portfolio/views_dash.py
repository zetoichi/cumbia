from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from .mixins import GeneralContextMixin
from .models import (
    Photographer,
    Pic,
)

class DashIndexView(GeneralContextMixin, TemplateView):
    template_name = 'portfolio/dash_index.html'


class DashAddPicsView(GeneralContextMixin, DetailView):
    template_name = 'portfolio/dash_add_pics.html'
    model = Photographer
