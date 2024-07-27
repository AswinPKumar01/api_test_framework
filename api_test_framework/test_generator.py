import jsonschema
from requests.exceptions import JSONDecodeError

class TestGenerator:
    def __init__(self, config):
        self.config = config

    def generate_tests(self):
        tests = []
        for endpoint in self.config.get_endpoints():
            for test_case in self.config.get_test_data():
                tests.append({
                    'endpoint': endpoint['path'],
                    'method': endpoint['method'],
                    'data': test_case.get('data'),
                    'expected_status': test_case.get('expected_status', 200),
                    'response_schema': endpoint.get('response_schema')
                })
        return tests

    def validate_response(self, response, schema):
        if not response.text.strip():
            return False

        try:
            response_json = response.json()
        except JSONDecodeError:
            return False
        
        try:
            jsonschema.validate(instance=response_json, schema=schema)
            return True
        except jsonschema.exceptions.ValidationError:
            return False
