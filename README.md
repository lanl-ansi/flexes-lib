# lanlytics-api-lib
[![Build Status](https://ci.lanlytics.com/nisac/lanlytics-api-lib.svg?token=RmFwLDimUxzrPXXq8Kti&branch=master)](https://ci.lanlytics.com/nisac/lanlytics-api-lib) [![codecov](https://cov.lanlytics.com/ghe/nisac/lanlytics-api-lib/branch/master/graph/badge.svg)](https://cov.lanlytics.com/ghe/nisac/lanlytics-api-lib)

Helper library for communicating with the lanlytics API

### Dependencies
For asynchronous task execution Python >= 3.5 is required.

### Usage at a glance
To run a task through the API synchronously
```python
from job import run_task

url = 'https://api.lanlytics.com'
message = {'service': 'echo-test', 'test': True}
result = run_task(url, message)
print(result['status'])
# active
```
