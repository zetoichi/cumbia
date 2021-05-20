from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponse,
)

from .models import Photographer, Pic

# path: 'dash/phs/<str:pk>/save/'
def save_new_pics(request: HttpRequest, pk: str) -> JsonResponse:
    ph = Photographer.objects.get(pk=pk)

    files = [
        request.FILES.get(f'pic[{i}]') for i in range(0, len(request.FILES))
    ]

    try:
        pics_created = ph.pics_from_files(files)
    except Exception as e:
        return HttpResponse(status=415)

    return JsonResponse(data={'pics_created': pics_created}, status=200)
