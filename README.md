# Unit Testing Project

This project focuses on understanding and implementing unit tests and integration tests in Python using the `unittest` framework. The goal is to master testing patterns including mocking, parametrization, and fixtures while following Python best practices.

## Learning Objectives

By the end of this project, you should be able to explain without external help:

- **The difference between unit and integration tests**
- **Common testing patterns such as mocking, parametrizations and fixtures**

## Concepts Overview

### Unit Testing

Unit testing is the process of testing that a particular function returns expected results for different sets of inputs. Key characteristics:

- Tests **standard inputs and corner cases**
- Should **only test the logic defined inside the tested function**
- **Most calls to additional functions should be mocked**, especially network or database calls
- Answers the question: *"If everything defined outside this function works as expected, does this function work as expected?"*

### Integration Testing

Integration tests aim to test a code path end-to-end:

- **Only low-level functions** that make external calls (HTTP requests, file I/O, database I/O) are mocked
- Tests **interactions between every part of your code**
- Validates that different components work together correctly

## Requirements

### Environment
- All files interpreted/compiled on **Ubuntu 18.04 LTS** using **Python 3** (version 3.7)
- All files should **end with a new line**
- First line of all files: `#!/usr/bin/env python3`

### Code Style
- Use **pycodestyle** style (version 2.5)
- All files must be **executable**

### Documentation
- A `README.md` file at the root of the project folder is **mandatory**
- All **modules** should have documentation
- All **classes** should have documentation  
- All **functions** (inside and outside classes) should have documentation
- Documentation must be **real sentences** explaining the purpose, not just simple words
- All functions and coroutines must be **type-annotated**

### Documentation Testing
You can verify documentation exists using:

```bash
# Module documentation
python3 -c 'print(__import__("my_module").__doc__)'

# Class documentation
python3 -c 'print(__import__("my_module").MyClass.__doc__)'

# Function documentation
python3 -c 'print(__import__("my_module").my_function.__doc__)'
python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'
```

## Running Tests

Execute your tests using the unittest module:

```bash
$ python -m unittest path/to/test_file.py
```

## Key Testing Patterns

### 1. Mocking
- **Purpose**: Replace dependencies with controlled fake objects
- **When to use**: External calls (APIs, databases, file systems)
- **Library**: `unittest.mock`

### 2. Parametrization
- **Purpose**: Run the same test with different input values
- **When to use**: Testing multiple scenarios efficiently
- **Library**: `parameterized`

### 3. Fixtures
- **Purpose**: Set up and tear down test environments
- **When to use**: Common test setup/cleanup operations
- **Methods**: `setUp()`, `tearDown()`, `setUpClass()`, `tearDownClass()`

## Resources

### Official Documentation
- [unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)
- [unittest.mock — mock object library](https://docs.python.org/3/library/unittest.mock.html)

### Additional Resources
- [How to mock a readonly property with mock?](https://stackoverflow.com/questions/17013172/how-to-mock-a-readonly-property-with-mock)
- [parameterized](https://pypi.org/project/parameterized/)
- [Memoization](https://en.wikipedia.org/wiki/Memoization)

## Project Structure

```
project_root/
├── README.md
├── utils.py                 # Utility functions to be tested
├── client.py               # Client class with external dependencies
├── test_utils.py           # Unit tests for utils.py
├── test_client.py          # Unit tests for client.py
└── test_integration.py     # Integration tests
```

## Example Test Structure

### Unit Test Example
```python
#!/usr/bin/env python3
"""Unit tests for utility functions."""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized

class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def setUp(self) -> None:
        """Set up test fixtures before each test method."""
        pass
    
    @parameterized.expand([
        (1, 2, 3),
        (0, 0, 0),
        (-1, 1, 0),
    ])
    def test_add_numbers(self, a: int, b: int, expected: int) -> None:
        """Test addition function with various inputs."""
        pass
    
    @patch('module.external_function')
    def test_function_with_external_call(self, mock_external: Mock) -> None:
        """Test function that makes external calls."""
        pass

if __name__ == '__main__':
    unittest.main()
```

## Best Practices

1. **Test Naming**: Use descriptive test method names that explain what is being tested
2. **Test Independence**: Each test should be independent and not rely on other tests
3. **Mock External Dependencies**: Always mock network calls, database operations, and file I/O
4. **Test Edge Cases**: Include tests for boundary conditions and error scenarios
5. **Clear Assertions**: Use specific assertion methods (`assertEqual`, `assertRaises`, etc.)
6. **Documentation**: Every test class and method should have clear docstrings

## Common Pitfalls to Avoid

- **Over-mocking**: Don't mock everything; only mock external dependencies
- **Testing Implementation Details**: Focus on testing behavior, not internal implementation
- **Brittle Tests**: Avoid tests that break when refactoring code that doesn't change behavior
- **Missing Edge Cases**: Always test boundary conditions and error scenarios

---

This project will help you build a solid foundation in Python testing practices that are essential for writing maintainable and reliable code.