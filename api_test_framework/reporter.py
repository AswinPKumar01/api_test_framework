import json
from datetime import datetime

class Reporter:
    def __init__(self):
        self.results = []

    def add_results(self, results):
        self.results.extend(results)

    def generate_report(self):
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results if result['pass'])
        failed_tests = total_tests - passed_tests

        report = {
            'timestamp': datetime.now().isoformat(),
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'success_rate': (passed_tests / total_tests) * 100 if total_tests > 0 else 0,
            'results': self.results
        }

        return json.dumps(report, indent=2)

    def save_report(self, filename='report.json'):
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)

    def print_summary(self):
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results if result['pass'])
        failed_tests = total_tests - passed_tests

        print(f"Total tests: {total_tests}")
        print(f"Passed tests: {passed_tests}")
        print(f"Failed tests: {failed_tests}")
        print(f"Success rate: {(passed_tests / total_tests) * 100:.2f}%" if total_tests > 0 else "N/A")