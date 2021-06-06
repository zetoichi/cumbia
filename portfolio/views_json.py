from typing import Type

from django.db import models
from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponse,
)

from .managers import SortableManager
from .models import Photographer, Pic

GET_METHOD_RESPONSE = JsonResponse(
    {'result': 'This view does not handle get requests, sorry'},
    status=400
)
EXCEPTION_500_RESPONSE = JsonResponse(
    {'result': 'Something went horribly wrong'},
    status=500
)
EXCEPTION_415_RESPONSE = HttpResponse(status=415)
SORT_SUCCESS_RESPONSE = JsonResponse({'result': 'Object sorted'}, status=200)

# path: 'phs/savepics/<str:pk>/'
def save_new_pics(request: HttpRequest, pk: str) -> JsonResponse:
    response = GET_METHOD_RESPONSE

    if request.method == 'POST':
        try:
            ph = Photographer.objects.get(pk=pk)
            files = [
                request.FILES.get(f'pic[{i}]') for i in range(0, len(request.FILES))
            ]
            pics_created = ph.pics_from_files(files)
            response = JsonResponse(
                data={'pics_created': pics_created},
                status=200
            )
        except Exception as e:
            response = EXCEPTION_415_RESPONSE

    return response

# path: 'phs/sort/'
def sort_ph(request: HttpRequest) -> JsonResponse:
    obj_model = Photographer
    manager = Photographer.objects
    return sort_object(obj_model, manager, request)

# path: 'phs/sortpics/<str:pk>/'
def sort_pic(request: HttpRequest, pk: str) -> JsonResponse:
    obj_model = Pic
    ph = Photographer.objects.get(pk=pk)
    manager = ph.pics
    return sort_object(obj_model, manager, request)


def sort_object(obj_model: Type[models.Model], manager: Type[SortableManager],
                request: HttpRequest) -> JsonResponse:
    response = GET_METHOD_RESPONSE

    if request.method == 'POST':
        try:
            manager.insort(
                obj=obj_model.objects.get(pk=request.POST.get('obj_pk')),
                new_idx=int(request.POST.get('new_idx'))
            )
            response = SORT_SUCCESS_RESPONSE
        except Exception as e:
            print(e)
            response = EXCEPTION_500_RESPONSE

    return response
