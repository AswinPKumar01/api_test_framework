import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_request(self, method, endpoint, data=None, params=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, json=data, params=params, headers=headers)
        return response