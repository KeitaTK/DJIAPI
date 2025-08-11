from django.shortcuts import render, redirect
from .services import ping_cloud_api
from django.contrib.auth.decorators import login_required
from .forms import DJICredentialsForm
from .models import UserDJICredentials

@login_required
def edit_credentials(request):
    creds, created = UserDJICredentials.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = DJICredentialsForm(request.POST, instance=creds)
        if form.is_valid():
            form.save()
            return redirect('dji_api:status')
    else:
        form = DJICredentialsForm(instance=creds)
    return render(request, 'dji_api/edit_credentials.html', {'form': form})

@login_required
def status_page(request):
    try:
        status = ping_cloud_api(request.user)
    except RuntimeError:
        return redirect('dji_api:edit_credentials')
    return render(request, 'dji_api/status.html', {'status': status})