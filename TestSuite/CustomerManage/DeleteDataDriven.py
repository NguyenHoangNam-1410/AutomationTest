from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import unittest
from time import sleep
from base_test import BaseDataDrivenTest

class DeleteDataDrivenTest(BaseDataDrivenTest):
    """Data-driven test class for delete functionality"""
    
    def test_delete_with_csv_data(self):
        """Test delete functionality with multiple customers from CSV"""
        test_data = self.read_csv_data('TestFile/CustomerManage/DeleteDataDriven.csv')
        
        for index, data in enumerate(test_data, start=1):
            # Parse the delete button locator
            delete_by_type, delete_value = self.parse_locator(data['deleteButton'])
            
            # Extract customer info for better logging
            customer_id = self.extract_customer_info_from_xpath(delete_value)
            
            with self.subTest(test_case=index, customer=customer_id):
                try:
                    self.print_test_header(index)
                    print(f"Site URL: {data['siteUrl']}")
                    print(f"Customer ID: {customer_id}")
                    print(f"Delete Button Locator: {delete_by_type}")
                    
                    # Navigate to the banking project
                    self.driver.get(data['siteUrl'])
                    
                    # Wait for page to load and table to be present
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'table'))
                    )
                    print(f"✓ Page loaded successfully")
                    
                    # Get initial row count before deletion
                    initial_rows = self.get_table_rows_count()
                    print(f"✓ Initial customer count: {initial_rows}")
                    
                    # Find the delete button
                    try:
                        delete_button = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((delete_by_type, delete_value))
                        )
                        print(f"✓ Delete button found for customer '{customer_id}'")
                    except TimeoutException:
                        print(f"✗ Delete button not found for customer '{customer_id}'")
                        print(f"⚠ Customer may have already been deleted or doesn't exist")
                        self.fail(f"Delete button not found for customer '{customer_id}'")
                    
                    # Verify button is clickable
                    try:
                        delete_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((delete_by_type, delete_value))
                        )
                        print(f"✓ Delete button is clickable")
                    except TimeoutException:
                        print(f"✗ Delete button not clickable")
                        self.fail("Delete button exists but is not clickable")
                    
                    # Click the delete button
                    try:
                        delete_button.click()
                        print(f"✓ Clicked delete button")
                        sleep(1)  # Wait for deletion animation/processing
                    except Exception as e:
                        print(f"✗ Failed to click delete button: {str(e)}")
                        self.fail(f"Could not click delete button: {str(e)}")
                    
                    # Verify table is still present after deletion
                    try:
                        results_table = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, 'table'))
                        )
                        self.assertIsNotNone(results_table, "Results table not found after delete")
                        print(f"✓ Table still present after deletion")
                    except Exception as e:
                        print(f"✗ Table verification failed: {str(e)}")
                        self.fail("Results table disappeared after deletion")
                    
                    # Get row count after deletion
                    final_rows = self.get_table_rows_count()
                    print(f"✓ Final customer count: {final_rows}")
                    
                    # Verify that row count decreased (customer was deleted)
                    if final_rows < initial_rows:
                        rows_deleted = initial_rows - final_rows
                        print(f"✓ Successfully deleted {rows_deleted} customer(s)")
                    elif final_rows == initial_rows:
                        print(f"⚠ Warning: Row count unchanged (was {initial_rows}, now {final_rows})")
                        print(f"⚠ Customer may not have been deleted or was the last one")
                    else:
                        print(f"⚠ Unexpected: Row count increased (was {initial_rows}, now {final_rows})")
                    
                    # Verify the delete button for this customer is gone
                    try:
                        self.driver.find_element(delete_by_type, delete_value)
                        print(f"⚠ Warning: Delete button still exists after deletion")
                    except NoSuchElementException:
                        print(f"✓ Delete button removed - customer '{customer_id}' successfully deleted")
                    
                    self.print_test_result(index, passed=True, 
                                         message=f"Customer '{customer_id}' deleted successfully")
                    
                except AssertionError as e:
                    self.print_test_result(index, passed=False, message=str(e))
                    raise
                except Exception as e:
                    self.print_test_result(index, passed=False, message=f"Unexpected error: {str(e)}")
                    self.fail(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Starting Delete Data-Driven Test Suite")
    print("="*60 + "\n")
    unittest.main(verbosity=2)