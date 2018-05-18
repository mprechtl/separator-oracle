
from Crypto.Cipher import AES
from separator_oracle.base.models import ActiveSession
import binascii


# keys which are used within a cookie
session_id_in_cookie = 'session_id'
secret_key_id_in_cookie = 'secret_key_id'

# to decode keys
utf_8 = 'utf-8'


class HasSession:

    def __init__(self, hasSession=False, correctness=False, error=None):
        self.hasSession = hasSession
        self.correctness = correctness
        self.error = error


########################################################################################
#                           Check Session Correctness
########################################################################################


def checkCorrectnessOfSession(request):
    if session_id_in_cookie in request.COOKIES and secret_key_id_in_cookie in request.COOKIES:
        # extract session id and secret key id from cookie
        sessionId = request.COOKIES[session_id_in_cookie]
        secretKeyId = request.COOKIES[secret_key_id_in_cookie]

        plain_session_id = decryptSession(sessionId, secretKeyId)

        if plain_session_id is None:
            return HasSession(True, False, buildWrongSessionError())

        # check if session attributes are correct; check amount of separators, ...
        return HasSession(True, True)
    else:
        return HasSession(False, False, buildInvalidSessionError())


########################################################################################
#                                   Decryption
########################################################################################


def decryptSession(sessionId, secretKeyId):
    try:
        session = ActiveSession.objects.get(secret_key_id=secretKeyId)

        # Get nonce and secret key from active session by transmitting secret key id
        nonce = session.nonce
        secret_key = session.secret_key
        session_id_bytes = binascii.a2b_base64(sessionId)

        # decrypt session id
        plain = decrypt(session_id_bytes, secret_key, nonce)
        return plain.decode(utf_8)
    except:
        return None


def decrypt(cipher_bytes, secret_key, nonce):
    cipher = AES.new(bytes(secret_key, encoding=utf_8),
                     AES.MODE_CTR, nonce=bytes(nonce, encoding=utf_8))
    return cipher.decrypt(cipher_bytes)


########################################################################################
#                               Error Types
########################################################################################

def buildInvalidSessionError():
    errorType = 'InvalidSession'
    msg = 'There is no session id or secret key identifier available.'
    return buildError(msg, errorType)


def buildWrongSessionError():
    errorType = 'InvalidSession'
    msg = 'The session id or secret key identifier is not correct.'
    return buildError(msg, errorType)


def buildError(msg='An unknown error occurred.', errorType='UnknownError'):
    return {'result': {'error': errorType, 'message': msg}}
