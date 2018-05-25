# Generated by Django 2.0.5 on 2018-05-25 23:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveSession',
            fields=[
                ('secret_key_id', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('secret_key', models.BinaryField(max_length=64)),
                ('nonce', models.BinaryField(max_length=64)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
