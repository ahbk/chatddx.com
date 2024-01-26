from django.http import JsonResponse, HttpResponse
from .models import OpenAIChat


def index(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    payload = OpenAIChat.objects.get(identifier="mock_1").serialize()
    return JsonResponse(payload)
