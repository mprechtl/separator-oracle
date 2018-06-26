
from django.db import models
from django.contrib.auth.models import User
import os
import base64


utf_8 = 'utf-8'


class ActiveSession(models.Model):
    secret_key_id = models.CharField(max_length=64, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    secret_key = models.BinaryField(max_length=64)
    nonce = models.BinaryField(max_length=64)

    @classmethod
    def create(cls, user, secret_key, nonce):
        possible_key_id = None
        key_is_used = True

        # check if generated secret key id is already used
        # generate a new one if it is already used
        while key_is_used:
            possible_key_id = base64.b64encode(os.urandom(32))
            try:
                ActiveSession.objects.get(secret_key_id=possible_key_id)
            except ActiveSession.DoesNotExist:
                key_is_used = False

        possible_key_id = possible_key_id.decode(utf_8)
        session = cls(secret_key_id=possible_key_id, user=user,
                      secret_key=secret_key, nonce=nonce)
        return session

    def get_secret_key_id(self):
        return self.secret_key_id

    def __str__(self):
        return '%s' % self.secret_key_id
