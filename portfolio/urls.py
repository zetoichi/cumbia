from django.urls import path

from . import (
    views_auth,
    views_main,
    views_json,
)

app_name = 'portfolio'

# AUTH
urlpatterns = [
    path(
        'login/',
        views_auth.CumbiaLoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        views_auth.cumbia_logout,
        name='logout'
    ),
]

# PUBLIC
urlpatterns += [
    path(
        '',
        views_main.IndexView.as_view(),
        name='index'
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
        'phs/detail/<str:pk>/',
        views_main.PhDetailView.as_view(),
        name='ph_detail'
    ),
    path(
        'phs_alt/detail/<str:pk>/',
        views_main.PhDetailAltView.as_view(),
        name='ph_detail_alt'
    ),
]

# PRIVATE
urlpatterns += [
    path(
        'phs/new/',
        views_main.PhCreateView.as_view(),
        name='ph_create'
    ),
    path(
        'phs/edit_pics/<str:pk>/',
        views_main.PhEditPicsView.as_view(),
        name='ph_edit_pics'
    ),
    path(
        'phs/add_pics/<str:pk>/',
        views_main.PhAddPicsView.as_view(),
        name='ph_add_pics'
    ),
]

# JSON
urlpatterns += [
    path(
        'phs/delpic/',
        views_json.delete_pic,
        name='ph_delete_pic'
    ),
    path(
        'phs/markmain/<str:pk>/',
        views_json.mark_pic_as_main,
        name='ph_mark_pic_as_main'
    ),
    path(
        'phs/savepics/<str:pk>/',
        views_json.save_new_pics,
        name='ph_save_pics'
    ),
    path(
        'phs/sort/',
        views_json.sort_ph,
        name='ph_sort'
    ),
    path(
        'phs/sortpics/<str:pk>/',
        views_json.sort_pic,
        name='ph_sort_pics'
    ),
]
