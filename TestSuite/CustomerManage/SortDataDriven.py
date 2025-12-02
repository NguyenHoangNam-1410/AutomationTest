from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
from time import sleep
from base_test import BaseDataDrivenTest

class SortDataDrivenTest(BaseDataDrivenTest):
    """Data-driven test class for sort functionality"""
    
    def test_sort_with_csv_data(self):
        """Test sort functionality with multiple sort options from CSV"""
        test_data = self.read_csv_data('TestFile/CustomerManage/SortDataDriven.csv')
        
        for index, data in enumerate(test_data, start=1):
            # Parse the sort label locator
            sort_by_type, sort_value = self.parse_locator(data['sortLabel'])
            
            with self.subTest(test_case=index, sort_label=sort_value):
                try:
                    self.print_test_header(index)
                    print(f"Site URL: {data['siteUrl']}")
                    print(f"Sort By: {sort_value}")
                    print(f"Sort Locator Type: {sort_by_type}")
                    
                    # Navigate to the banking project
                    self.driver.get(data['siteUrl'])
                    
                    # Wait for page to load
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'table'))
                    )
                    print(f"✓ Page loaded successfully")
                    
                    # Get table data before sorting (optional - for verification)
                    try:
                        table_before = self.driver.find_element(By.TAG_NAME, 'table')
                        rows_before = len(table_before.find_elements(By.TAG_NAME, 'tr'))
                        print(f"✓ Table found with {rows_before} rows (including header)")
                    except Exception as e:
                        print(f"⚠ Warning: Could not count table rows: {str(e)}")
                    
                    # Click on the sort link/button
                    try:
                        sort_element = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((sort_by_type, sort_value))
                        )
                        sort_element.click()
                        print(f"✓ Clicked sort element: '{sort_value}'")
                        sleep(1)  # Wait for sort animation/processing
                    except Exception as e:
                        print(f"✗ Failed to click sort element: {str(e)}")
                        self.fail(f"Sort element not found or not clickable: {sort_value}")
                    
                    # Verify table is still present after sorting
                    try:
                        results_table = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, 'table'))
                        )
                        self.assertIsNotNone(results_table, "Results table not found after sort")
                        print(f"✓ Table still present after sorting")
                    except Exception as e:
                        print(f"✗ Table verification failed: {str(e)}")
                        self.fail("Results table disappeared after sorting")
                    
                    # Verify customer button exists using parsed locator
                    try:
                        button_by_type, button_value = self.parse_locator(data['customerButton'])
                        customer_button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((button_by_type, button_value))
                        )
                        self.assertIsNotNone(customer_button, "Customer button not found")
                        print(f"✓ Customer button verified")
                    except Exception as e:
                        print(f"⚠ Customer button verification failed: {str(e)}")
                    
                    self.print_test_result(index, passed=True, 
                                         message=f"Successfully sorted by: '{sort_value}'")
                    
                except AssertionError as e:
                    self.print_test_result(index, passed=False, message=str(e))
                    raise
                except Exception as e:
                    self.print_test_result(index, passed=False, message=f"Unexpected error: {str(e)}")
                    self.fail(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("Starting Sort Data-Driven Test Suite")
    print("="*60 + "\n")
    unittest.main(verbosity=2)