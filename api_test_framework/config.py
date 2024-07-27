import yaml
from typing import Dict, Any

class Config:
    def __init__(self, config_file: str):
        with open(config_file, 'r') as file:
            self.config: Dict[str, Any] = yaml.safe_load(file)

    def get_base_url(self) -> str:
        return self.config['base_url']

    def get_endpoints(self) -> list:
        return self.config['endpoints']

    def get_test_data(self) -> list:
        return self.config['test_data']

    def get_headers(self) -> Dict[str, str]:
        return self.config.get('headers', {})

    def get_auth(self) -> Dict[str, str]:
        return self.config.get('auth', {})