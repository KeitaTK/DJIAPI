from django.urls import path
from . import views

app_name = 'dji_api'
urlpatterns = [
  path('status/', views.status_page, name='status'),
  # 他のURL定義…
]
