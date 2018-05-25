
from Crypto.Cipher import AES
from django.contrib.auth.models import User
from separator_oracle.base.models import ActiveSession
import os
import base64
import traceback

username_key = '_Username'
password_key = '_Password'
valid_until_key = '_Valid'

utf_8 = 'utf-8'


class UserData:

    def __init__(self, username, password, valid_until):
        self.username = username
        self.password = password
        self.valid_until = valid_until


def createUserData(args):
    if len(args) == 6 and username_key in args and password_key in args and valid_until_key in args:
        index_of_username_key = args.index(username_key)
        index_of_password_key = args.index(password_key)
        index_of_valid_key = args.index(valid_until_key)

        if index_of_password_key < 5 and index_of_username_key < 5 and index_of_valid_key < 5:
            username = args[index_of_username_key + 1]
            password = args[index_of_password_key + 1]
            valid_until = args[index_of_valid_key + 1]

            return UserData(username, password, valid_until)

    msg = 'You have to provide an username, a password and a date (YYYY-MM-DD)!'
    raise ValueError(msg)


def saveUser(user_data):
    # create user
    user = User.objects.create_user(
        username=user_data.username, password=user_data.password)
    user.save()
    return user


def saveSession(user, secret_key, nonce):
    # create new active session
    session = ActiveSession.create(user, secret_key, nonce)
    session.save()
    return session


def run(*args):
    # Specify username, password and validity of generated session token
    user_data = createUserData(args)

    # secret key and nonce!
    secret_key = os.urandom(16)  # 16 bytes
    nonce = os.urandom(8)  # 8 bytes
    aes = AES.new(secret_key, AES.MODE_CTR, nonce=nonce)

    # build plaintext and encrypt it
    plaintext = user_data.username + ";" + \
        user_data.password + ";" + user_data.valid_until
    ciphertext = aes.encrypt(bytes(plaintext, encoding=utf_8))

    # get bytes of ciphertext and encode it as base64 string
    bytes_of_ciphertext = bytearray(ciphertext)
    ciphertext_base64 = base64.b64encode(bytes_of_ciphertext).decode(utf_8)

    try:
        user = saveUser(user_data)
        session = saveSession(user, secret_key, nonce)

        # print session id and secret key
        print('Your session_id : %s' % ciphertext_base64)
        print('Your secret_key_id: %s' % session.get_secret_key_id())
    except:
        traceback.print_exc()
