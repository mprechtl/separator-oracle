
from Crypto.Cipher import AES
from separator_oracle.base.models import ActiveSession
import binascii

utf_8 = 'utf-8'


def decryptSession(sessionId, secretKeyId):
    session = ActiveSession.objects.get(secret_key_id=secretKeyId)

    # Get nonce and secret key from active session by transmitting secret key id
    nonce = session.nonce
    secret_key = session.secret_key
    session_id_bytes = binascii.a2b_base64(sessionId)

    # decrypt session id
    plain = decrypt(session_id_bytes, secret_key, nonce)
    return plain.decode(utf_8)


def decrypt(cipher_bytes, secret_key, nonce):
    cipher = AES.new(bytes(secret_key, encoding=utf_8),
                     AES.MODE_CTR, nonce=bytes(nonce, encoding=utf_8))
    return cipher.decrypt(cipher_bytes)
