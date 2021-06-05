from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

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

class PhCreateView(GeneralContextMixin, CreateView):
    template_name = 'portfolio/ph_create.html'
    model = Photographer
    segment = 'detail'
    fields = (
        'first_name',
        'last_name',
        'display_name',
        'bio'
    )

    def post(self, request):
        form = self.get_form()

        if form.is_valid():
            data = form.cleaned_data
            ph = self.model.objects.create(**data)
            return redirect(
                reverse_lazy('portfolio:ph_detail',
                args=[ph.pk]
                )
            )

class PhDetailView(GeneralContextMixin, DetailView):
    template_name = 'portfolio/ph_detail.html'
    model = Photographer
    context_object_name = 'ph'
    segment = 'detail'

class PhEditPicsView(PhDetailView):
    template_name = 'portfolio/ph_edit_pics.html'

class PhAddPicsView(PhDetailView):
    template_name = 'portfolio/ph_add_pics.html'

class PhDetailAltView(PhDetailView):
    template_name = 'portfolio/ph_detail_alt.html'  # TEMP VIEW: DELETE!!!
