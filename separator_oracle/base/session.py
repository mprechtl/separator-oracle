
from Crypto.Cipher import AES
from separator_oracle.base.models import ActiveSession
import binascii
import datetime
import traceback


# keys which are used within a cookie
session_id_in_cookie = 'session_id'
secret_key_id_in_cookie = 'secret_key_id'

# to decode keys
utf_8 = 'utf-8'
latin_1 = 'ISO 8859-1'


class HasSession:

    def __init__(self, hasSession=False, correct=False, error=None, status_code=400):
        self.hasSession = hasSession
        self.correct = correct
        self.error = error
        self.status_code = status_code


########################################################################################
#                           Check Session Correctness
########################################################################################


def checkCorrectnessOfSession(request):
    if session_id_in_cookie in request.COOKIES and secret_key_id_in_cookie in request.COOKIES:
        # extract session id and secret key id from cookie
        sessionId = request.COOKIES[session_id_in_cookie]
        secretKeyId = request.COOKIES[secret_key_id_in_cookie]

        try:
            session_to_secret_key_id = ActiveSession.objects.get(
                secret_key_id=secretKeyId)
        except ActiveSession.DoesNotExist:
            return HasSession(True, False, buildWrongSessionError())

        # check if decryption did work
        auto_login_cookie = decryptSession(session_to_secret_key_id, sessionId)
        if auto_login_cookie is None:
            return HasSession(True, False, buildWrongSessionError())

        # check if session attributes are correct; check amount of separators, ...
        if auto_login_cookie.count(";") != 2:
            return HasSession(True, False, buildSeparatorError())
        username, password, valid_until = auto_login_cookie.split(";")

        # check if date is valid
        if valid_until.count("-") != 2:
            return HasSession(True, False, buildUnvalidDateError(), status_code=418)
        year, month, day = valid_until.split("-")

        # check if every value is an integer
        if not isInteger(year) or not isInteger(month) or not isInteger(day):
            return HasSession(True, False, buildWrongSessionError())

        user = session_to_secret_key_id.user
        today = datetime.date.today()  # maybe replace with datetime
        valid_until_date = datetime.date(
            int(year), int(month), int(day))  # maybe add time

        # Process username, password and valid until
        correct_username = user.get_username() == username
        correct_password = user.check_password(password)
        valid = valid_until_date > today

        if correct_username and correct_password and valid:
            return HasSession(True, True, status_code=200)
        else:
            return HasSession(True, False, buildWrongSessionError())
    else:
        return HasSession(False, False, buildInvalidSessionError())


# method to check if a string represents an int
def isInteger(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

########################################################################################
#                                   Decryption
########################################################################################


def decryptSession(session, sessionId):
    try:
        # Get nonce and secret key from active session by transmitting secret key id
        nonce = session.nonce
        secret_key = session.secret_key
        session_id_bytes = binascii.a2b_base64(sessionId)

        # decrypt session id
        plain = decrypt(session_id_bytes, secret_key, nonce)
        return plain.decode(latin_1)
    except:
        traceback.print_exc()
        return None


def decrypt(cipher_bytes, secret_key, nonce):
    cipher = AES.new(secret_key, AES.MODE_CTR, nonce=nonce)
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


def buildUnvalidDateError():
    errorType = 'InvalidSession'
    msg = 'The provided date is not valid.'
    return buildError(msg, errorType)


def buildSeparatorError():
    errorType = 'ValueError'
    msg = 'Invalid number of separators.'
    return buildError(msg, errorType)


def buildError(msg='An unknown error occurred.', errorType='UnknownError'):
    return {'result': {'error': errorType, 'message': msg}}
