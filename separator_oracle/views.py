
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse


def index(request):
    if request.method == 'GET':
        response = JsonResponse({'result': 'Index of Separator Oracle'})
        return response
    else:
        return HttpResponseNotAllowed(['GET'])
