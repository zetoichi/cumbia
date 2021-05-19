from django.urls import path

from . import (
    views_main,
    views_json,
)

# CBV

urlpatterns = [
    path(
        '',
        views_main.IndexView.as_view(),
        name='public_index'
    ),
    path(
        'phs/<str:pk>/',
        views_main.PhDetailView.as_view(),
        name='ph_detail'
    ),
]

# JSON

urlpatterns += [
    path(
        'dash/phs/save/<str:pk>/',
        views_json.save_new_pics,
        name='dash_ph_save_pics'
    ),
]
