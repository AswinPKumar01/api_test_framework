import json
import csv
import os
from datetime import datetime
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader

class Reporter:
    def __init__(self):
        self.results: List[Dict[str, Any]] = []
        self.output_dir: str = self._create_output_directory()

    def _create_output_directory(self) -> str:
        base_dir = os.path.join(os.getcwd(), 'test_outputs')
        if not os.path.exists(base_dir):
            os.mkdir(base_dir)
        
        # Create a new directory for this test run
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = os.path.join(base_dir, f"test_run_{timestamp}")
        os.mkdir(run_dir)
        return run_dir

    def add_results(self, results: List[Dict[str, Any]]):
        self.results.extend(results)

    def generate_report(self) -> str:
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

    def save_json_report(self, filename: str = 'report.json'):
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)

    def save_csv_report(self, filename: str = 'report.csv'):
        if not self.results:
            return

        filepath = os.path.join(self.output_dir, filename)
        keys = self.results[0].keys()
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.results)

    def save_html_report(self, filename: str = 'report.html'):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('report_template.html')
        
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results if result['pass'])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0

        html_content = template.render(
            timestamp=datetime.now().isoformat(),
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            success_rate=success_rate,
            results=self.results
        )

        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w') as f:
            f.write(html_content)

    def print_summary(self):
        total_tests = len(self.results)
        passed_tests = sum(1 for result in self.results if result['pass'])
        failed_tests = total_tests - passed_tests

        print(f"Total tests: {total_tests}")
        print(f"Passed tests: {passed_tests}")
        print(f"Failed tests: {failed_tests}")
        print(f"Success rate: {(passed_tests / total_tests) * 100:.2f}%" if total_tests > 0 else "N/A")
        print(f"Reports saved in: {self.output_dir}")