# Automated API Testing Framework

## Overview

This project is an **Automated API Testing Framework** built with Python. It is designed to facilitate the testing of APIs by providing an easy-to-use framework for defining, running, and reporting test cases. The framework leverages the `requests` library for API interactions and `pytest` for test execution.

## Project Structure

```
api_test_framework/
│
├── api_test_framework/
│   ├── __init__.py           # Initialization file for the package
│   ├── config.py             # Configuration settings for the framework
│   ├── api_client.py         # API client for making HTTP requests
│   ├── test_generator.py     # Module for generating test cases
│   ├── test_runner.py        # Module for executing test cases
│   └── reporter.py           # Module for generating test reports
│
├── tests/
│   └── test_sample_api.py    # Sample test cases for demonstration
│
├── run_tests.py              # Script to run the test suite
├── config.yaml               # Configuration file for API endpoints and settings
└── requirements.txt          # Python dependencies
```

## Features

- **Dynamic Test Case Generation**: Automatically generates test cases based on API specifications.
- **Parallel Test Execution**: Supports running tests in parallel to speed up execution.
- **Comprehensive Reporting**: Provides detailed reports on test results.
- **Easy Configuration**: Configure API endpoints and test settings via a YAML file.
- **Customizable**: Easily extendable to support additional features or modifications.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/AswinPKumar01/api_test_framework.git
   cd api_test_framework
   ```

2. **Create and activate a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Configure your API endpoints and other settings in the `config.yaml` file. This file should be located in the root of your project directory. Below is an example configuration:

```yaml
api_endpoints:
  base_url: "https://api.example.com"
  endpoints:
    - name: "Get User"
      url: "/users/{user_id}"
      method: "GET"
      expected_status: 200
    - name: "Create User"
      url: "/users"
      method: "POST"
      expected_status: 201
```

## Running Tests

To run the test suite, use the `run_tests.py` script:

```bash
python run_tests.py
```

This script will execute all test cases defined in the `tests` directory and generate a report.

## Writing Tests

1. **Define a Test Case**: Create a new test file in the `tests/` directory. Use the following structure:

   ```python
   from api_test_framework.api_client import APIClient
   from api_test_framework.test_generator import TestGenerator

   def test_sample_api():
       client = APIClient()
       test_cases = TestGenerator.generate_test_cases()
       
       for test_case in test_cases:
           response = client.make_request(test_case)
           assert response.status_code == test_case.expected_status
   ```

2. **Run Tests**: Execute the test suite to run your new tests and view the results.

## Version

This is an initial version of the application. More features and integrations will be updated soon.

