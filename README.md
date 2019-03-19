<<<<<<< HEAD
# lanlytics-cloud-utils

[![Build Status](https://ci.lanlytics.com/nisac/lanlytics-cloud-utils.svg?token=RmFwLDimUxzrPXXq8Kti&branch=master)](https://ci.lanlytics.com/nisac/lanlytics-cloud-utils) [![codecov](https://cov.lanlytics.com/ghe/nisac/lanlytics-cloud-utils/branch/master/graph/badge.svg)](https://cov.lanlytics.com/ghe/nisac/lanlytics-cloud-utils)

General utilities for communicating with cloud platforms
=======
# lanlytics-api-lib
[![Build Status](https://ci.lanlytics.com/nisac/lanlytics-api-lib.svg?token=RmFwLDimUxzrPXXq8Kti&branch=master)](https://ci.lanlytics.com/nisac/lanlytics-api-lib) 
[![codecov](https://cov.lanlytics.com/ghe/nisac/lanlytics-api-lib/branch/master/graph/badge.svg)](https://cov.lanlytics.com/ghe/nisac/lanlytics-api-lib)

Helper library for communicating with the lanlytics API

### Dependencies
For asynchronous task execution Python >= 3.5 is required.

### Usage at a glance
To run a task through the API synchronously
```python
from lanlytics_api_lib.job import run_task

message = {'service': 'echo-test', 'test': True}
result = run_task(message)
print(result['status'])
# active
```

Asynchronous tasks are also supported
```python
from asyncio import get_event_loop
from lanlytics_api_lib.async_job import run_task

message = {'service': 'echo-test', 'test': True}
result = loop.run_until_complete(run_task(message))
print(result['status'])
# active
```

The nice thing about asynchronous tasks is that you can run them in parallel.
This example submits three jobs in parallel and then waits for all three to
complete before returning the results.
```python
from asyncio import gather, get_event_loop
from lanlytics_api_lib.async_job import run_task

m1 = {'service': 'echo-test', 'test': True}
m2 = {'service': 'echo-test', 'test': True}
m3 = {'service': 'echo-test', 'test': True}
results = loop.run_until_complete(
    gather(
        run_task(m1),
        run_task(m2),
        run_task(m3)
    )
)
print([result['status'] for result in results])
# ['active', 'active', 'active']
```
>>>>>>> api-lib/master
