# Automation Test Suite

## Installation

1. **Install Python** (3.7+)
2. **Install dependencies:**
   ```
   pip install selenium
   ```

3. **Download WebDriver** - Download the appropriate driver for your browser (ChromeDriver for Chrome)

## Project Structure

- `base_test.py` - Base test class with common methods
- `TestSuite/` - Contains all test suite files
- `TestFile/` - Contains CSV data files for data-driven testing

## Running Tests

```
python TestSuite/SearchDataDriven.py
python TestSuite/SortDataDriven.py
python TestSuite/DeleteDataDriven.py
```

## Adding a New Test Suite

1. Create a new Python file in `TestSuite/` folder (e.g., `NewTestSuite.py`)
2. Import base_test class:
   ```python
   from base_test import BaseTest
   ```
3. Create your test class and inherit from BaseTest
4. Write your test methods
5. Run the test file

## Adding Test Data

- Create a new CSV file in `TestFile/` folder
- Reference it in your test suite
- Use data-driven approach similar to existing tests

## Example Test Case

```python
from base_test import BaseTest

class NewTest(BaseTest):
    def test_example(self):
        # Your test code here
        pass

if __name__ == '__main__':
    test = NewTest()
    test.test_example()
```
