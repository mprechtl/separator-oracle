
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from .base import session


def index(request):
    # Check if GET-method is used
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    # Check if session id is used
    has_session = session.checkCorrectnessOfSession(request)

    if has_session.hasSession and has_session.correct:
        # Do something :)
        return JsonResponse({'result': {'message': 'Everything is fine.'}})
    else:
        return JsonResponse(has_session.error, status=has_session.status_code)
