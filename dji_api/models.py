# dji_api/models.py
from django.db import models
class DJICloudToken(models.Model):
    access_token  = models.CharField(max_length=255, blank=True)
    refresh_token = models.CharField(max_length=255, blank=True)
    expires_at   = models.DateTimeField()
    updated_at   = models.DateTimeField(auto_now=True)
