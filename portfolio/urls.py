from django.urls import path

from . import (
    public_views,
    dash_views,
)

urlpatterns = [
    path('', public_views.PublicIndexView.as_view(), name='public_index'),
    path('dash/', dash_views.DashIndexView.as_view(), name='dash_index'),
]
