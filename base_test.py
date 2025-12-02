"""
Base Test Class and Utilities for Data-Driven Testing
Provides reusable components for Banking Project automation tests
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import unittest
import csv
import os


class LocatorParser:
    """Utility class for parsing locator strings"""
    
    @staticmethod
    def parse(locator_string):
        """
        Parse Katalon/Selenium IDE style locator string
        
        Args:
            locator_string (str): Locator in format 'type=value' 
                                 (e.g., 'xpath=//input', 'id=search', 'link=First Name')
            
        Returns:
            tuple: (By type, locator value)
        """
        # Strip whitespace
        locator_string = locator_string.strip()
        
        # Remove outer quotes if present (handles CSV quoting)
        if (locator_string.startswith('"') and locator_string.endswith('"')) or \
           (locator_string.startswith("'") and locator_string.endswith("'")):
            locator_string = locator_string[1:-1]
        
        if '=' in locator_string:
            locator_type, locator_value = locator_string.split('=', 1)
            locator_type = locator_type.lower().strip()
            locator_value = locator_value.strip()
            
            # Remove quotes from locator value if present
            if (locator_value.startswith('"') and locator_value.endswith('"')) or \
               (locator_value.startswith("'") and locator_value.endswith("'")):
                locator_value = locator_value[1:-1]
            
            # Map Katalon/Selenium IDE locator types to Selenium By types
            locator_map = {
                'id': By.ID,
                'name': By.NAME,
                'xpath': By.XPATH,
                'link': By.LINK_TEXT,
                'linktext': By.LINK_TEXT,
                'partiallinktext': By.PARTIAL_LINK_TEXT,
                'css': By.CSS_SELECTOR,
                'cssselector': By.CSS_SELECTOR,
                'classname': By.CLASS_NAME,
                'tagname': By.TAG_NAME
            }
            
            by_type = locator_map.get(locator_type, By.XPATH)
            return by_type, locator_value
        else:
            # If no prefix, treat as XPath
            return By.XPATH, locator_string


class CSVDataReader:
    """Utility class for reading CSV test data"""
    
    @staticmethod
    def read(filename, base_path=None):
        """
        Read test data from CSV file
        
        Args:
            filename (str): Path to CSV file (relative or absolute)
            base_path (str): Base directory path (optional)
            
        Returns:
            list: List of dictionaries containing test data
        """
        test_data = []
        
        # Determine the file path
        if base_path:
            csv_path = os.path.join(base_path, filename)
        elif not os.path.isabs(filename):
            # Use the calling script's directory as base
            import inspect
            caller_frame = inspect.stack()[1]
            caller_file = caller_frame.filename
            current_dir = os.path.dirname(os.path.abspath(caller_file))
            csv_path = os.path.join(current_dir, filename)
        else:
            csv_path = filename
        
        try:
            with open(csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    test_data.append(row)
            print(f"✓ Successfully loaded {len(test_data)} test cases from {os.path.basename(filename)}")
        except FileNotFoundError:
            print(f"✗ Error: File not found - {csv_path}")
            raise
        except Exception as e:
            print(f"✗ Error reading CSV: {str(e)}")
            raise
        
        return test_data


class BaseDataDrivenTest(unittest.TestCase):
    """Base class for data-driven tests with common functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Set up browser once for all tests with proper Chrome options"""
        # Configure Chrome options to suppress popups and notifications
        chrome_options = Options()
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--no-default-browser-check")
        # Uncomment to run in headless mode (no UI):
        # chrome_options.add_argument("--headless")
        
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.implicitly_wait(10)
        cls.driver.maximize_window()
        print("\n✓ Browser initialized with proper Chrome options")
    
    @classmethod
    def tearDownClass(cls):
        """Close browser after all tests"""
        print("\n" + "="*60)
        print("Test execution completed. Closing browser...")
        print("="*60)
        cls.driver.quit()
    
    def parse_locator(self, locator_string):
        """
        Parse locator string using LocatorParser utility
        
        Args:
            locator_string (str): Locator in format 'type=value'
            
        Returns:
            tuple: (By type, locator value)
        """
        return LocatorParser.parse(locator_string)
    
    def read_csv_data(self, filename):
        """
        Read test data from CSV file using CSVDataReader utility
        
        Args:
            filename (str): Path to CSV file
            
        Returns:
            list: List of dictionaries containing test data
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))
        return CSVDataReader.read(filename, base_path=current_dir)
    
    def get_table_rows_count(self):
        """
        Get the number of visible rows in the table (excluding header)
        
        Returns:
            int: Number of data rows in table
        """
        try:
            table = self.driver.find_element(By.TAG_NAME, 'table')
            rows = table.find_elements(By.TAG_NAME, 'tr')
            # Subtract 1 for header row
            return len(rows) - 1 if len(rows) > 0 else 0
        except Exception as e:
            print(f"⚠ Could not count table rows: {str(e)}")
            return 0
    
    def print_test_header(self, test_case_num, title="Test Case"):
        """Print formatted test case header"""
        print(f"\n{'='*60}")
        print(f"{title} {test_case_num}")
        print(f"{'='*60}")
    
    def print_test_result(self, test_case_num, passed=True, message=""):
        """Print formatted test result"""
        print(f"{'='*60}")
        if passed:
            print(f"✓✓✓ Test Case {test_case_num} PASSED ✓✓✓")
            if message:
                print(f"    {message}")
        else:
            print(f"✗✗✗ Test Case {test_case_num} FAILED ✗✗✗")
            if message:
                print(f"    Error: {message}")
        print(f"{'='*60}")
    
    def extract_customer_info_from_xpath(self, xpath):
        """
        Extract customer identifier from XPath (e.g., post code or name)
        
        Args:
            xpath (str): XPath containing customer info
            
        Returns:
            str: Customer identifier or 'Unknown'
        """
        try:
            # Try to extract text from normalize-space patterns
            # Example: (.//*[normalize-space(text()) and normalize-space(.)='E55555'])
            if "normalize-space(.)='" in xpath:
                start = xpath.find("normalize-space(.)='") + len("normalize-space(.)='")
                end = xpath.find("']", start)
                if end > start:
                    return xpath[start:end]
            return "Unknown"
        except Exception:
            return "Unknown"
