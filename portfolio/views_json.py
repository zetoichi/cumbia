from lorem_text import lorem

from django.http import (
    HttpRequest,
    JsonResponse,
    HttpResponse,
)

from .models import Pic

# path: 'dash/phs/<str:pk>/save/'
def save_new_pics(request: HttpRequest, pk: str) -> JsonResponse:
    pass
