#!/usr/bin/env python3
"""
Test runner for ATS Score Checker.
"""
import unittest
import sys
import os

def run_tests():
    """Run all test cases."""
    # Add src directory to Python path
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    sys.path.insert(0, src_dir)
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return 0 if tests passed, 1 if any failed
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    sys.exit(run_tests()) 