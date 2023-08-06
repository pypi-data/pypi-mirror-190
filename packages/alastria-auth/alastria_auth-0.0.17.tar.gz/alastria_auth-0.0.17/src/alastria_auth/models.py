from django.db import models
from datetime import timedelta
from django.utils.timezone import now


class RequestSession(models.Model):
    request_date = models.DateTimeField()
    expiration_date = models.DateTimeField(verbose_name="Expirate date")
    requested_by = models.CharField(max_length=255)
    qr_code = models.ImageField()
    confirm_url = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)


class ApiSession(models.Model):

    token = models.CharField(max_length=1255)
    expiration_date = models.DateTimeField(verbose_name="Expirate date")
    is_active = models.BooleanField(default=True)
    request_session_id = models.IntegerField()
    extra_info = models.JSONField(blank=True, null=True)
