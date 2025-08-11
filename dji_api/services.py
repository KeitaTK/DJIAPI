# dji_api/services.py

import requests
import urllib3
import ssl
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
from django.utils import timezone
from .models import DJICloudToken, UserDJICredentials

# 開発環境: InsecureRequestWarning を抑制
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_BASE = 'https://api.djicloud.com/v1'

class TLS12Adapter(HTTPAdapter):
    """
    TLS1.2 固定かつホスト名チェック無効化の Adapter
    """
    def init_poolmanager(self, *args, **kwargs):
        # TLS1.2 以上のみ許可
        ctx = create_urllib3_context()
        ctx.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        # ホスト名チェックと証明書検証を無効化
        ctx.check_hostname = False
        ctx.verify_mode    = ssl.CERT_NONE
        kwargs['ssl_context'] = ctx
        return super().init_poolmanager(*args, **kwargs)

def get_session():
    """
    TLS12Adapter を使ったセッションを返す
    """
    session = requests.Session()
    session.mount('https://', TLS12Adapter())
    return session

def refresh_user_token(user):
    creds = user.dji_credentials
    payload = {
        'app_id':     creds.app_id,
        'app_key':    creds.app_key,
        'grant_type': 'client_credentials',
    }
    session = get_session()
    # verify=False は不要になりました
    res = session.post(f'{API_BASE}/oauth/token', json=payload)
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
    headers   = {'Authorization': f'Bearer {token_obj.access_token}'}
    session = get_session()
    res = session.get(f'{API_BASE}/devices', headers=headers, timeout=5)
    res.raise_for_status()
    return {
        'ping_success': True,
        'ping_error':   None,
        'expires_at':   token_obj.expires_at,
    }
