#!/usr/bin/env python3
# @author: AI Assistant
# Script to run all tests in the project

import os
import subprocess
import sys

def run_tests():
    """
    Run all tests in the project using pytest.
    """
    print("Running all tests in the project...")
    
    # Run pytest with verbose output and collect coverage data
    result = subprocess.run(
        ["python3", "-m", "pytest", "-v", "--cov=."],
        capture_output=True,
        text=True
    )
    
    # Print the output
    print(result.stdout)
    
    if result.stderr:
        print("Errors:", file=sys.stderr)
        print(result.stderr, file=sys.stderr)
    
    # Return the exit code
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)