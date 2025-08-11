# dji_api/services.py
import requests
from django.conf import settings
from django.utils import timezone
from .models import DJICloudToken

API_BASE = 'https://api.djicloud.com/v1'

def ping_cloud_api():
    """
    1) トークンの有効期限チェック
    2) テストエンドポイント呼び出し（例: デバイス一覧取得）
    戻り値: {
      'token_valid': bool,
      'expires_at': datetime,
      'ping_success': bool,
      'ping_error': str or None,
      'timestamp': datetime
    }
    """
    now = timezone.now()
    token_obj = DJICloudToken.objects.first()
    token_valid = token_obj and token_obj.expires_at > now

    result = {
        'token_valid': token_valid,
        'expires_at': token_obj.expires_at if token_obj else None,
        'ping_success': False,
        'ping_error': None,
        'timestamp': now,
    }
    if not token_valid:
        result['ping_error'] = 'Access token expired or not found'
        return result

    headers = {'Authorization': f'Bearer {token_obj.access_token}'}
    try:
        # テスト用にデバイス一覧取得エンドポイントを呼び出し
        url = f"{API_BASE}/devices"
        res = requests.get(url, headers=headers, timeout=5)
        res.raise_for_status()
        result['ping_success'] = True
    except Exception as e:
        result['ping_error'] = str(e)

    return result
