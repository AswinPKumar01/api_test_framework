import concurrent.futures
from typing import List, Dict, Any
from api_test_framework.api_client import APIClient

class TestRunner:
    def __init__(self, config, test_generator):
        self.config = config
        self.test_generator = test_generator
        self.api_client = APIClient(self.config.get_base_url(), self.config.get_headers(), self.config.get_auth())

    def run_test(self, test: Dict[str, Any]) -> Dict[str, Any]:
        response = self.api_client.send_request(
            test['method'],
            test['endpoint'],
            data=test.get('data'),
            params=test.get('params'),
            headers=test.get('headers')
        )
        
        if response is None:
            return {
                'endpoint': test['endpoint'],
                'method': test['method'],
                'pass': False,
                'error': 'Request failed'
            }

        result = {
            'endpoint': test['endpoint'],
            'method': test['method'],
            'status_code': response.status_code,
            'expected_status': test['expected_status'],
            'pass': response.status_code == test['expected_status']
        }

        if test['response_schema']:
            schema_valid = self.test_generator.validate_response(response, test['response_schema'])
            result['schema_valid'] = schema_valid
            result['pass'] = result['pass'] and schema_valid

        return result

    def run_tests(self, max_workers: int = 5) -> List[Dict[str, Any]]:
        tests = self.test_generator.generate_tests()
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_test = {executor.submit(self.run_test, test): test for test in tests}
            for future in concurrent.futures.as_completed(future_to_test):
                results.append(future.result())

        return results