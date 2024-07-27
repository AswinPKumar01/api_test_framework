from api_test_framework.config import Config
from api_test_framework.test_generator import TestGenerator
from api_test_framework.test_runner import TestRunner
from api_test_framework.reporter import Reporter

def main():
    config = Config('config.yaml')
    test_generator = TestGenerator(config)
    test_runner = TestRunner(config, test_generator)
    reporter = Reporter()

    results = test_runner.run_tests()
    reporter.add_results(results)
    
    reporter.print_summary()
    reporter.save_report()

if __name__ == '__main__':
    main()