# 4. サービス層を修正
# ファイル: dji_api/services.py

import requests
from django.utils import timezone
from .models import DJICloudToken, UserDJICredentials

API_BASE = 'https://api.djicloud.com/v1'

def get_user_credentials(user):
    try:
        return user.dji_credentials
    except UserDJICredentials.DoesNotExist:
        raise RuntimeError('DJI認証情報が設定されていません')

def refresh_user_token(user):
    creds = get_user_credentials(user)
    payload = {
        'app_id':     creds.app_id,
        'app_key':    creds.app_key,
        'grant_type': 'client_credentials',
    }
    res = requests.post(f'{API_BASE}/oauth/token', json=payload)
    res.raise_for_status()
    data = res.json()

    token_obj, _ = DJICloudToken.objects.get_or_create(id=user.id)
    token_obj.access_token  = data['access_token']
    token_obj.refresh_token = data.get('refresh_token', '')
    token_obj.expires_at    = timezone.now() + timezone.timedelta(seconds=data.get('expires_in', 0))
    token_obj.save()
    return token_obj

def ping_cloud_api(user):
    token_obj = refresh_user_token(user)
    headers = {'Authorization': f'Bearer {token_obj.access_token}'}
    try:
        res = requests.get(f'{API_BASE}/devices', headers=headers, timeout=5)
        res.raise_for_status()
        return {
            'ping_success': True,
            'ping_error':   None,
            'expires_at':   token_obj.expires_at
        }
    except Exception as e:
        return {
            'ping_success': False,
            'ping_error':   str(e),
            'expires_at':   token_obj.expires_at
        }
