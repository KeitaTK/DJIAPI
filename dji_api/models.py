# dji_api/models.py
class DJICloudToken(models.Model):
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    expires_at   = models.DateTimeField()
    updated_at   = models.DateTimeField(auto_now=True)
