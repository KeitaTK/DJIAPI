from django.contrib import admin
from .models import DJICloudToken

@admin.register(DJICloudToken)
class DJICloudTokenAdmin(admin.ModelAdmin):
    list_display = ('access_token', 'expires_at', 'updated_at')
