from lorem_text import lorem

from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponse,
)

from .models import Pic

# path: 'dash/phs/<str:pk>/save/'
def save_new_pics(request: HttpRequest, pk: str) -> JsonResponse:
    ph = Pic.objects.get(pk=pk)

    files = [
        request.FILES.get('file[%d]' % i) for i in range(0, len(request.FILES))
    ]

    for f in files:
        new_pic = Pic.objects.create(
            pic=f,
            photographer=ph,
            caption=lorem.words(8)
        )

    return JsonResponse({'status': 200})
