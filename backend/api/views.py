from django.http import JsonResponse

from .models import OpenAIChat

def index(request):
    payload = OpenAIChat.objects.get(identifier="mock_1").serialize()
    return JsonResponse(payload)

