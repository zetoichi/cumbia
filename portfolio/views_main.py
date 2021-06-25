from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView
)
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .signals import see_this
from .mixins import (
    GeneralContextMixin,
    UserDetailMixin,
    PhDetailMixin,
    GalleryMixin,
)
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

class PhDetailView(GeneralContextMixin, PhDetailMixin,
        DetailView):
    template_name = 'portfolio/ph_detail.html'
    creating = False
    segment = 'detail'

class PhPicsDetailView(GalleryMixin, PhDetailView):
    sub_segment = 'pics'
    gallery = {
        'type': 'horizontal',
        'path': 'portfolio/components/galleries/pics.html'
    }

class PhVideoDetailView(GalleryMixin, PhDetailView):
    sub_segment = 'videos'
    gallery = {
        'type': 'horizontal',
        'path': 'portfolio/components/galleries/videos.html'
    }

class PhAllDetailView(GalleryMixin, PhDetailView):
    sub_segment = 'all'
    gallery = {
        'type': 'center',
        'path': 'portfolio/components/galleries/all.html'
    }

##
# CRUD
##

class UserCreateView(GeneralContextMixin, UserDetailMixin,
        CreateView):
    template_name = 'portfolio/user_create.html'
    segment = 'edit'
    creating = False
    success_url = reverse_lazy('portfolio:index')

    def form_valid(self, form):
        data = self.clean_password(form.cleaned_data)
        user = self.model.objects.create_superuser(**data)
        return redirect(self.success_url)

    def clean_password(self, data):
        pw = data['password1']
        if data.pop('password1') == data.pop('password2'):
            data['password'] = pw
        return data

class PhCreateView(GeneralContextMixin, PhDetailMixin,
        CreateView):
    template_name = 'portfolio/ph_create.html'
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

class PhEditView(GeneralContextMixin, PhDetailMixin,
        UpdateView):
    template_name = 'portfolio/ph_edit.html'
    segment = 'edit'
    creating = False

    def dispatch(self, request, pk, *args, **kwargs):
        if self.request.session.get('creating'):
            self.creating = True
        return super().dispatch(request, pk, *args, **kwargs)

    def get_success_url(self):
        args = [self.get_object().pk]
        url = 'portfolio:ph_detail_pics'
        if self.request.session['creating']:
            url = 'portfolio:ph_create_confirm'
        return reverse_lazy(url, args=args)

class PhCreateConfirmView(GeneralContextMixin, PhDetailMixin,
        DetailView):
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
                    'portfolio:ph_detail_pics', args=[pk]
                )
            )

class PhDeleteView(GeneralContextMixin, PhDetailMixin,
        DeleteView):
    template_name = 'portfolio/ph_delete_confirm.html'
    segment = 'edit'
    creating = False
    success_url = reverse_lazy('portfolio:index')

class PhAddPicsView(GeneralContextMixin, PhDetailMixin,
        DetailView):
    template_name = 'portfolio/ph_add_pics.html'
    segment = 'edit'
    creating = False

class PhAddFirstPicsView(GeneralContextMixin, PhDetailMixin,
        DetailView):
    template_name = 'portfolio/ph_add_first_pics.html'
    segment = 'edit'
    creating = True
