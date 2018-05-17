
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from .base import session

session_id_in_cookie = 'session_id'
secret_key_id_in_cookie = 'secret_key_id'


def index(request):
    # Check if GET-method is used
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    # Check if session id is used
    if session_id_in_cookie not in request.COOKIES and secret_key_id_in_cookie not in request.COOKIES:
        return buildInvalidSessionMsg()
    else:
        sessionId = request.COOKIES[session_id_in_cookie]
        secretKeyId = request.COOKIES[secret_key_id_in_cookie]
        session.checkSession(sessionId, secretKeyId)

        # Do something :)
        return JsonResponse({'result': {'message': 'Everything is fine.'}})


def buildInvalidSessionMsg():
    return JsonResponse({'result': {'error': 'InvalidSession', 'message': 'There is no session id or secret key identifier available.'}})
