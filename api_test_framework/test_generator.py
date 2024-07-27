import jsonschema
from typing import List, Dict, Any

class TestGenerator:
    def __init__(self, config):
        self.config = config

    def generate_tests(self) -> List[Dict[str, Any]]:
        tests = []
        for endpoint in self.config.get_endpoints():
            for test_case in self.config.get_test_data():
                tests.append({
                    'endpoint': endpoint['path'],
                    'method': endpoint['method'],
                    'data': test_case.get('data'),
                    'params': test_case.get('params'),
                    'headers': test_case.get('headers'),
                    'expected_status': test_case.get('expected_status', 200),
                    'response_schema': endpoint.get('response_schema')
                })
        return tests

    def validate_response(self, response, schema) -> bool:
        try:
            jsonschema.validate(instance=response.json(), schema=schema)
            return True
        except jsonschema.exceptions.ValidationError as e:
            print(f"Schema validation error: {e}")
            return False