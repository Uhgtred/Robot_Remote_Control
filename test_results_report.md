# Test Results Report

## Summary
- **Total Tests**: 36
- **Passed**: 28 (78%)
- **Failed**: 5 (14%)
- **Errors**: 3 (8%)
- **Warnings**: 1
- **Test Coverage**: 79%

## Issues Identified

### 1. Network-Related Errors
Some tests failed because they tried to bind to specific IP addresses that don't exist in the Docker container:
```
OSError: [Errno 99] Cannot assign requested address
```
This occurred in `BusTransactions/UnitTests/test_BusFactory.py` and `BusTransactions/UnitTests/test_BusTransceiver.py` when trying to bind to IP address 192.168.178.32.

### 2. Fixture Errors
Tests in `Runners/test_UnitTests/test_asyncRunner.py` expected a 'sleepTime' fixture that wasn't found:
```
fixture 'sleepTime' not found
```

### 3. Attribute Errors
Tests in `Events/UnitTests/test_Event.py` failed due to attribute name mismatches:
```
AttributeError: 'AbstractEvent' object has no attribute '_Event__subscribers'. Did you mean: '_AbstractEvent__subscribers'?
```

### 4. Logging Errors
There were I/O operations on closed files in the logging system:
```
ValueError: I/O operation on closed file.
```

## Recommendations

1. **Fix Network Binding Issues**: 
   - Modify the tests to use '0.0.0.0' or '127.0.0.1' instead of specific IP addresses when running in Docker.
   - Consider using environment variables to determine the appropriate IP address based on the environment.

2. **Fix Fixture Issues**:
   - Update the test functions in `test_asyncRunner.py` to properly define or use fixtures.
   - Consider converting the functions to use pytest's parameterization instead of fixtures.

3. **Fix Attribute Name Mismatches**:
   - Update the tests in `test_Event.py` to use the correct attribute names.
   - Ensure that the tests are updated when class implementations change.

4. **Fix Logging Issues**:
   - Ensure that logging handlers are properly closed before the program exits.
   - Consider using a context manager for logging to ensure proper cleanup.

## Conclusion
The majority of tests (78%) are passing successfully, which is a good sign. The failing tests are related to specific issues that can be addressed with targeted fixes. The overall test coverage of 79% is good, but there's room for improvement, especially in modules like `main.py` which has 0% coverage.