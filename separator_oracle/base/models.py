
from django.db import models
from django.contrib.auth.models import User


class ActiveSession(models.Model):
    secret_key_id = models.CharField(max_length=64, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    secret_key = models.CharField(max_length=64)
    nonce = models.CharField(max_length=64)

    def __str__(self):
        return '%s' % self.secret_key_id
