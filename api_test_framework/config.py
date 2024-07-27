import yaml

class Config:
    def __init__(self, config_file):
        with open(config_file, 'r') as file:
            self.config = yaml.safe_load(file)

    def get_base_url(self):
        return self.config['base_url']

    def get_endpoints(self):
        return self.config['endpoints']

    def get_test_data(self):
        return self.config['test_data']