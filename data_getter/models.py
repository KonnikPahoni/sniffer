from django.db import models
from logging import WARNING


class User(models.Model):
    telegram_id = models.IntegerField(unique=True, db_index=True)
    name = models.CharField(max_length=255)
    roles_csv = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    registered = models.DateTimeField(auto_now_add=True)


class Dataset(models.Model):
    handler_name = models.CharField(max_length=255)
    current_status = models.CharField(max_length=15)
    interval = models.IntegerField()
    last_update = models.DateTimeField(auto_now_add=True)
    day_started = models.DateTimeField(auto_now_add=True)
    public_name = models.CharField(max_length=255)
    tags_csv = models.CharField(max_length=1000)
    description = models.TextField()
    image = models.FileField(upload_to='public/images/')
    added_by = models.ForeignKey('User', on_delete=models.CASCADE)


class AdminSettings(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, primary_key=True)
    logging_level = models.SmallIntegerField(default=WARNING)


class GetterModel(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, unique=True, db_index=True)


# TODO: Import migrations from schemas AUTOMATICALLY
from data_getter.schemas.bfx import *
