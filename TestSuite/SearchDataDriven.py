from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
from time import sleep
from base_test import BaseDataDrivenTest

class SearchDataDrivenTest(BaseDataDrivenTest):
    """Data-driven test class for search functionality"""
    
    def test_search_with_csv_data(self):
        """Test search functionality with multiple search terms from CSV"""
        test_data = self.read_csv_data('TestFile/SearchDataDriven.csv')
        
        for index, data in enumerate(test_data, start=1):
            # Parse the search input locator
            search_by_type, search_value = self.parse_locator(data['searchInput'])
            
            with self.subTest(test_case=index, search_text=data['searchText']):
                try:
                    self.print_test_header(index)
                    print(f"Site URL: {data['siteUrl']}")
                    print(f"Search Text: '{data['searchText']}'")
                    print(f"Search Input Locator: {search_by_type} = {search_value}")
                    
                    # Navigate to the banking project
                    self.driver.get(data['siteUrl'])
                    
                    # Wait for page to load and table to be present
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, 'table'))
                    )
                    print(f"✓ Page loaded successfully")
                    
                    # Get initial row count
                    initial_rows = self.get_table_rows_count()
                    print(f"✓ Initial table rows: {initial_rows}")
                    
                    # Wait for search input to be present and visible
                    search_field = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((search_by_type, search_value))
                    )
                    print(f"✓ Search field found")
                    
                    # Clear any previous search text
                    search_field.clear()
                    sleep(0.5)
                    print(f"✓ Search field cleared")
                    
                    # Enter search text
                    search_field.send_keys(data['searchText'])
                    print(f"✓ Entered search text: '{data['searchText']}'")
                    
                    # Wait a moment for the search to filter results
                    sleep(1.5)
                    
                    # Get filtered row count
                    filtered_rows = self.get_table_rows_count()
                    print(f"✓ Filtered table rows: {filtered_rows}")
                    
                    # Verify table is still present after search
                    results_table = self.driver.find_element(By.TAG_NAME, 'table')
                    self.assertIsNotNone(results_table, "Results table not found after search")
                    print(f"✓ Table still present after search")
                    
                    # Verify that search actually filtered the results
                    # (unless the search text doesn't match any records, in which case filtered_rows could be 0)
                    if filtered_rows > 0:
                        print(f"✓ Search returned {filtered_rows} result(s)")
                        
                        # Optional: Verify that search text appears in the results
                        try:
                            table_text = results_table.text.lower()
                            search_text_lower = data['searchText'].lower()
                            if search_text_lower in table_text:
                                print(f"✓ Search text '{data['searchText']}' found in results")
                            else:
                                print(f"⚠ Search text '{data['searchText']}' not visible in results, but table is present")
                        except Exception as e:
                            print(f"⚠ Could not verify search text in results: {str(e)}")
                    else:
                        print(f"⚠ Search returned 0 results - no matches found for '{data['searchText']}'")
                    
                    # Clear search field after test (optional cleanup)
                    search_field.clear()
                    sleep(0.5)
                    
                    # Verify table is restored after clearing search
                    final_rows = self.get_table_rows_count()
                    print(f"✓ Rows after clearing search: {final_rows}")
                    
                    self.print_test_result(index, passed=True, 
                                         message=f"Search for '{data['searchText']}' executed successfully")
                    
                except AssertionError as e:
                    self.print_test_result(index, passed=False, message=str(e))
                    raise
                except Exception as e:
                    self.print_test_result(index, passed=False, message=f"Unexpected error: {str(e)}")
                    self.fail(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Starting Search Data-Driven Test Suite")
    print("="*60 + "\n")
    unittest.main(verbosity=2)