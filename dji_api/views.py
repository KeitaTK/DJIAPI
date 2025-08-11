# dji_api/views.py
from django.shortcuts import render
from .services import ping_cloud_api

def status_page(request):
    status = ping_cloud_api()
    return render(request, 'dji_api/status.html', {'status': status})
