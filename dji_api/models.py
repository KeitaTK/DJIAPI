from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DJICloudToken(models.Model):
    access_token  = models.CharField(max_length=255, blank=True)
    refresh_token = models.CharField(max_length=255, blank=True)
    expires_at    = models.DateTimeField()
    updated_at    = models.DateTimeField(auto_now=True)

class UserDJICredentials(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dji_credentials')
    app_id      = models.CharField('App ID', max_length=100)
    app_key     = models.CharField('App Key', max_length=255)
    app_license = models.CharField('App License', max_length=255, blank=True)

    def __str__(self):
        return f'{self.user.username} の DJI 認証情報'