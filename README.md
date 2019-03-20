# flexes-lib

[![Build Status](https://travis-ci.org/lanl-ansi/flexes-lib.svg?branch=master)](https://travis-ci.org/lanl-ansi/flexes-lib)
[![codecov](https://codecov.io/gh/lanl-ansi/flexes-lib/branch/master/graph/badge.svg)](https://codecov.io/gh/lanl-ansi/flexes-lib)

Client library for flexes

### Dependencies
For asynchronous task execution Python >= 3.5 is required.

### Usage at a glance
To run a task through the API synchronously
```python
from flexes_lib.job import run_task

message = {'service': 'echo-test', 'test': True}
result = run_task(message)
print(result['status'])
# active
```

Asynchronous tasks are also supported
```python
from asyncio import get_event_loop
from flexes_lib.async_job import run_task

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
from flexes_lib.async_job import run_task

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
