from django.urls import path

from . import (
    views_main,
    views_json,
)

app_name = 'portfolio'

# CBV
urlpatterns = [
    path(
        '',
        views_main.IndexView.as_view(),
        name='index'
    ),
    path(
        'login/',
        views_main.CumbiaLoginView.as_view(),
        name='login'
    ),
    path(
        'about/',
        views_main.AboutView.as_view(),
        name='about'
    ),
    path(
        'contact/',
        views_main.ContactView.as_view(),
        name='contact'
    ),
    path(
        'phs/<str:pk>/',
        views_main.PhDetailView.as_view(),
        name='ph_detail'
    ),
    path(
        'phs_alt/<str:pk>/',
        views_main.PhDetailAltView.as_view(),
        name='ph_detail_alt'
    ),
    path(
        'phs/<str:pk>/edit/',
        views_main.PhEditPicsView.as_view(),
        name='ph_edit_pics'
    ),
    path(
        'phs/<str:pk>/add/',
        views_main.PhAddPicsView.as_view(),
        name='ph_add_pics'
    ),
]

# JSON

urlpatterns += [
    path(
        'phs/savepics/<str:pk>/',
        views_json.save_new_pics,
        name='ph_save_pics'
    ),
]
