# aws-utils

[![Build Status](https://ci.lanlytics.com/nisac/aws-utils.svg?token=RmFwLDimUxzrPXXq8Kti&branch=master)](https://ci.lanlytics.com/nisac/aws-utils) [![codecov](https://cov.lanlytics.com/ghe/nisac/aws-utils/branch/master/graph/badge.svg)](https://cov.lanlytics.com/ghe/nisac/aws-utils)

General utilities for communicating with Amazon Web Services

## Installation
The best way to use this package in other projects is to add it as a submodule using git. To add a submodule in an existing git project via the command line run the following command in the root of your project.
```bash
$ git submodule add git@github.lanlytics.com:nisac/aws-utils.git aws_utils
```
This will create a folder `aws_utils` in the root of your project and copy the files there. After that you can install via `pip`. It is recommended you install inside of a virtual environment.
```bash
$ python3 -m venv env
$ source env/bin/activate
(env)$ pip install aws_utils/
```
If you would the package included in your `requirements.txt` file simply add `./aws_utils` to the requirements file. 

_Note: `pip freeze > requirements.txt` will erase the relative path_

Submodules are tied to a specific commit so if you would like the newest version of the package run the following command.
```bash
$ git submodule update --remote aws_utils
```
