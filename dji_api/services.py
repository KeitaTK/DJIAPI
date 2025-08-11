# dji_api/services.py

import requests
import urllib3
from django.utils import timezone
from .models import DJICloudToken, UserDJICredentials

# 開発環境での警告抑制
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_BASE = 'https://api.djicloud.com/v1'

def refresh_user_token(user):
    """
    アクセストークン取得エンドポイント呼び出し
    SSL 検証を一時的に無効化 (verify=False)
    """
    creds = user.dji_credentials
    payload = {
        'app_id':     creds.app_id,
        'app_key':    creds.app_key,
        'grant_type': 'client_credentials',
    }

    # verify=False で SSL 検証を無効化
    res = requests.post(
        f'{API_BASE}/oauth/token',
        json=payload,
        verify=False
    )
    res.raise_for_status()
    data = res.json()

    token_obj, _ = DJICloudToken.objects.get_or_create(id=user.id)
    token_obj.access_token  = data['access_token']
    token_obj.refresh_token = data.get('refresh_token', '')
    token_obj.expires_at    = timezone.now() + timezone.timedelta(
        seconds=data.get('expires_in', 0)
    )
    token_obj.save()
    return token_obj

def ping_cloud_api(user):
    """
    デバイスエンドポイント呼び出し
    SSL 検証を一時的に無効化 (verify=False)
    """
    token_obj = refresh_user_token(user)
    headers   = {'Authorization': f'Bearer {token_obj.access_token}'}

    res = requests.get(
        f'{API_BASE}/devices',
        headers=headers,
        timeout=5,
        verify=False
    )
    res.raise_for_status()

    return {
        'ping_success': True,
        'ping_error':   None,
        'expires_at':   token_obj.expires_at
    }
