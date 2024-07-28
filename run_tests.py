import argparse
import logging
from api_test_framework.config import Config
from api_test_framework.test_generator import TestGenerator
from api_test_framework.test_runner import TestRunner
from api_test_framework.reporter import Reporter

def setup_logging(level):
    logging.basicConfig(level=level, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    parser = argparse.ArgumentParser(description='Run API tests')
    parser.add_argument('--config', default='config.yaml', help='Path to the configuration file')
    parser.add_argument('--workers', type=int, default=5, help='Number of worker threads')
    parser.add_argument('--log-level', default='INFO', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        help='Set the logging level')
    args = parser.parse_args()

    setup_logging(logging.DEBUG)


    logging.info(f"Loading configuration from {args.config}")
    config = Config(args.config)
    test_generator = TestGenerator(config)
    test_runner = TestRunner(config, test_generator)
    reporter = Reporter()

    logging.info(f"Running tests with {args.workers} workers")
    results = test_runner.run_tests(max_workers=args.workers)
    reporter.add_results(results)
    
    reporter.print_summary()
    reporter.save_json_report()
    reporter.save_csv_report()
    reporter.save_html_report()
    logging.info(f"Test execution completed. Reports saved in {reporter.output_dir}")

if __name__ == '__main__':
    main()