import concurrent.futures
from api_test_framework.api_client import APIClient

class TestRunner:
    def __init__(self, config, test_generator):
        self.config = config
        self.test_generator = test_generator
        self.api_client = APIClient(self.config.get_base_url())

    def run_test(self, test):
        response = self.api_client.send_request(
            test['method'],
            test['endpoint'],
            data=test['data']
        )
        
        print(f"Response for {test['endpoint']} ({test['method']}): {response.text}")  # Debugging line

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

    def run_tests(self, max_workers=5):
        tests = self.test_generator.generate_tests()
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_test = {executor.submit(self.run_test, test): test for test in tests}
            for future in concurrent.futures.as_completed(future_to_test):
                results.append(future.result())

        return results