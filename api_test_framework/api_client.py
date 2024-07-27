import requests
from typing import Dict, Any, Optional

class APIClient:
    def __init__(self, base_url: str, default_headers: Dict[str, str] = None, auth: Dict[str, str] = None):
        self.base_url = base_url
        self.default_headers = default_headers or {}
        self.auth = auth

    def send_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, 
                     params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        request_headers = {**self.default_headers, **(headers or {})}
        
        auth = None
        if self.auth:
            auth = (self.auth.get('username'), self.auth.get('password'))

        try:
            response = requests.request(method, url, json=data, params=params, headers=request_headers, auth=auth)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return e.response if hasattr(e, 'response') else None

        return response