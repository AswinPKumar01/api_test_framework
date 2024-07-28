import concurrent.futures
import logging
from typing import List, Dict, Any
from api_test_framework.api_client import APIClient

class TestRunner:
    def __init__(self, config, test_generator):
        self.config = config
        self.test_generator = test_generator
        self.api_client = APIClient(self.config.get_base_url(), self.config.get_headers(), self.config.get_auth())

    def run_test(self, test: Dict[str, Any]) -> Dict[str, Any]:
        logging.info(f"Running test: {test['method']} {test['endpoint']}")
        logging.info(f"Request data: {test.get('data')}")
        logging.info(f"Request params: {test.get('params')}")
        logging.info(f"Request headers: {test.get('headers')}")

        try:
            response = self.api_client.send_request(
                test['method'],
                test['endpoint'],
                data=test.get('data'),
                params=test.get('params'),
                headers=test.get('headers')
            )
            
            if response is None:
                logging.error(f"Test failed: No response received for {test['method']} {test['endpoint']}")
                return {
                    'endpoint': test['endpoint'],
                    'method': test['method'],
                    'pass': False,
                    'error': 'No response received'
                }

            logging.info(f"Response status: {response.status_code}")
            logging.info(f"Response headers: {response.headers}")
            logging.info(f"Response body: {response.text[:200]}...")  # Log first 200 characters of response body

            result = {
                'endpoint': test['endpoint'],
                'method': test['method'],
                'status_code': response.status_code,
                'expected_status': test['expected_status'],
                'pass': response.status_code == test['expected_status'],
                'response_body': response.text
            }

            if test['response_schema']:
                schema_valid = self.test_generator.validate_response(response, test['response_schema'])
                result['schema_valid'] = schema_valid
                result['pass'] = result['pass'] and schema_valid
                if not schema_valid:
                    logging.warning(f"Schema validation failed for {test['method']} {test['endpoint']}")

            if not result['pass']:
                logging.warning(f"Test failed: expected status {test['expected_status']}, got {response.status_code}")

            return result

        except Exception as e:
            logging.error(f"Exception occurred while running test {test['method']} {test['endpoint']}: {str(e)}")
            return {
                'endpoint': test['endpoint'],
                'method': test['method'],
                'pass': False,
                'error': str(e)
            }

    def run_tests(self, max_workers: int = 5) -> List[Dict[str, Any]]:
        tests = self.test_generator.generate_tests()
        results = []

        logging.info(f"Starting test run with {len(tests)} tests using {max_workers} workers")

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_test = {executor.submit(self.run_test, test): test for test in tests}
            for future in concurrent.futures.as_completed(future_to_test):
                results.append(future.result())

        logging.info(f"Test run completed. Total tests: {len(results)}")

        return results