from lorem_text import lorem

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
        request.FILES.get('pic[%d]' % i) for i in range(0, len(request.FILES))
    ]

    pics_created = []
    try:
        for f in files:
            new_pic = Pic.objects.create(
                pic=f,
                photographer=ph,
                caption=lorem.words(6)
            )
            pics_created.append(new_pic.pk)
    except Exception as e:
        return HttpResponse(status=415)

    return JsonResponse(data={'pics_created': pics_created}, status=200)
