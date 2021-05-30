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
        name='public_index'
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
