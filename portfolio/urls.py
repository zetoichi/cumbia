from django.urls import path

from . import (
    views_public,
    views_dash,
    views_util,
)

# PUBLIC

urlpatterns = [
    path(
        '',
        views_public.PublicIndexView.as_view(),
        name='public_index'),
]

#  DASHBOARD

urlpatterns += [
    path(
        'dash/',
        views_dash.DashIndexView.as_view(),
        name='dash_index'),
    path(
        'dash/phs/add/<str:pk>/',
        views_dash.DashAddPicsView.as_view(),
        name='dash_ph_add_pics'
    ),
    path(
        'dash/phs/save/<str:pk>/',
        views_util.save_new_pics,
        name='dash_ph_save_pics'
    ),
]
