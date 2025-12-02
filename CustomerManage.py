"""
Unified Test Suite Runner
Runs all data-driven tests together
"""

import unittest
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from TestSuite.CustomerManage.SearchDataDriven import SearchDataDrivenTest
from TestSuite.CustomerManage.SortDataDriven import SortDataDrivenTest
from TestSuite.CustomerManage.DeleteDataDriven import DeleteDataDrivenTest


def create_test_suite():
    """Create a test suite with all data-driven tests"""
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SearchDataDrivenTest))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SortDataDrivenTest))
    test_suite.addTests(unittest.TestLoader().loadTestsFromTestCase(DeleteDataDrivenTest))
    
    return test_suite


def run_tests():
    """Run all tests with detailed reporting"""
    print("\n" + "=" * 70)
    print("DATA-DRIVEN TEST SUITE RUNNER")
    print("=" * 70)
    print("\nAvailable Tests:")
    print("  1. SearchDataDrivenTest - Tests search functionality")
    print("  2. SortDataDrivenTest   - Tests sort functionality")
    print("  3. DeleteDataDrivenTest - Tests delete functionality")
    print("\n" + "=" * 70)
    print("\nStarting test execution...\n")
    
    # Create test suite
    suite = create_test_suite()
    
    # Run tests with verbosity
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST EXECUTION SUMMARY")
    print("=" * 70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("=" * 70 + "\n")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
