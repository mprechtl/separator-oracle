
from Crypto.Cipher import AES
from separator_oracle.base.models import ActiveSession
import binascii

utf_8 = 'utf-8'


def checkSession(sessionId, secretKeyId):
    session = ActiveSession.objects.get(secret_key_id=secretKeyId)
    nonce = session.nonce
    secret_key = session.secret_key
    plain = decryptSession(sessionId, secret_key, nonce)
    print(plain.decode(utf_8))


def decryptSession(sessionId, secret_key, nonce):
    session_id_bytes = binascii.a2b_base64(sessionId)
    cipher = AES.new(bytes(secret_key, encoding=utf_8),
                     AES.MODE_CTR, nonce=bytes(nonce, encoding=utf_8))
    return cipher.decrypt(session_id_bytes)
