from django.urls import path

from . import (
    views_public,
    views_dash,
)

urlpatterns = [
    path('', views_public.PublicIndexView.as_view(), name='public_index'),
    path('dash/', views_dash.DashIndexView.as_view(), name='dash_index'),
    # path('dash/new-pics/', views_dash.DashIndexView.as_view(), name='dash_index'),
]
