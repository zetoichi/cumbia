from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .signals import see_this
from .mixins import GeneralContextMixin
from .models import (
    Photographer,
    Pic,
)
from .forms import PhotographerForm

class IndexView(GeneralContextMixin, TemplateView):
    template_name = 'portfolio/index.html'
    segment = 'index'
    creating = False

class AboutView(GeneralContextMixin, TemplateView):
    template_name = 'portfolio/about.html'
    segment = 'info'
    creating = False

class ContactView(GeneralContextMixin, TemplateView):
    template_name = 'portfolio/contact.html'
    segment = 'info'
    creating = False

class PhCreateView(GeneralContextMixin, CreateView):
    template_name = 'portfolio/ph_create.html'
    model = Photographer
    form_class = PhotographerForm
    segment = 'edit'
    creating = True

    def post(self, request):
        form = self.get_form()

        if form.is_valid():
            data = form.cleaned_data
            ph = self.model.objects.create(**data)
            return redirect(
                reverse_lazy('portfolio:ph_add_first',
                args=[ph.pk]
                )
            )

class PhEditView(GeneralContextMixin, UpdateView):
    template_name = 'portfolio/ph_edit.html'
    model = Photographer
    context_object_name = 'ph'
    form_class = PhotographerForm
    segment = 'edit'
    creating = False

    def dispatch(self, request, pk, *args, **kwargs):
        if self.request.session.get('creating'):
            self.creating = True
        return super().dispatch(request, pk, *args, **kwargs)

    def get_success_url(self):
        args = [self.get_object().pk]
        url = 'portfolio:ph_detail'
        if self.request.session['creating']:
            url = 'portfolio:ph_create_confirm'
        return reverse_lazy(url, args=args)

class PhDeleteView(GeneralContextMixin, DeleteView):
    template_name = 'portfolio/ph_delete_confirm.html'
    model = Photographer
    form_class = PhotographerForm
    context_object_name = 'ph'
    segment = 'edit'
    creating = False
    success_url = reverse_lazy('portfolio:index')

class PhPicsDetailView(GeneralContextMixin, DetailView):
    template_name = 'portfolio/ph_detail.html'
    model = Photographer
    context_object_name = 'ph'
    segment = 'detail'
    creating = False

class PhCreateConfirmView(PhPicsDetailView):
    template_name = 'portfolio/ph_create_confirm.html'
    segment = 'edit'
    creating = True

    def dispatch(self, request, pk, *args, **kwargs):
        if self.request.session.get('creating'):
            self.creating = True
            ph = self.get_object()
            ph.control_showable()
            return super().dispatch(request, pk, *args, **kwargs)
        else:
            return redirect(
                reverse_lazy(
                    'portfolio:ph_detail', args=[pk]
                )
            )

class PhAddPicsView(PhPicsDetailView):
    template_name = 'portfolio/ph_add_pics.html'
    segment = 'edit'
    creating = False

class PhAddFirstPicsView(PhPicsDetailView):
    template_name = 'portfolio/ph_add_first_pics.html'
    segment = 'edit'
    creating = True
