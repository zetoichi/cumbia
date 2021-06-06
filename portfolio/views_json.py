from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponse,
)

from .models import Photographer, Pic

# path: 'phs/savepics/<str:pk>/'
def save_new_pics(request: HttpRequest, pk: str) -> JsonResponse:
    if request.method == 'POST':
        ph = Photographer.objects.get(pk=pk)

        files = [
            request.FILES.get(f'pic[{i}]') for i in range(0, len(request.FILES))
        ]

        try:
            pics_created = ph.pics_from_files(files)
        except Exception as e:
            return HttpResponse(status=415)

        return JsonResponse(data={'pics_created': pics_created}, status=200)

    return JsonResponse({'r': 'This view does not handle get requests, sorry'})

# path: 'phs/sortpics/<str:pk>/'
def sort_pic(request: HttpRequest, pk: str) -> JsonResponse:
    response = JsonResponse(
        {'result': 'This view does not handle get requests, sorry'},
        status=400
    )

    if request.method == 'POST':
        try:
            ph = Photographer.objects.get(pk=pk)
            ph.insort_pic(
                pic=Pic.objects.get(pk=request.POST.get('pic_pk')),
                new_idx=int(request.POST.get('new_idx'))
            )
            response = JsonResponse({'result': 'Pic sorted'}, status=200)
        except Exception as e:
            response = JsonResponse({
                'result': 'Something went horribly wrong'},
                status=500
            )

    return response
