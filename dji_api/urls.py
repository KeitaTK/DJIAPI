# 5. URL 定義を修正
# ファイル: dji_api/urls.py

from django.urls import path
from . import views

app_name = 'dji_api'
urlpatterns = [
    path('credentials/', views.edit_credentials, name='edit_credentials'),
    path('status/',      views.status_page,      name='status'),
]
