from django.http import JsonResponse, HttpResponse
from .models import OpenAIChatCluster


def chat_cluster(request, cluster):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    payload = OpenAIChatCluster.objects.get(identifier=cluster).serialize()
    return JsonResponse(payload)
