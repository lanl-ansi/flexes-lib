from setuptools import setup

setup(name='aws_utils',
      description='Utilities for iteracting with Amazon Web Services',
      author='James Arnold',
      author_email='arnold_j@lanl.gov',
      version='0.1',
      packages=['aws_utils'],
      install_requires=['boto3', 'ujson']
      license='MIT')
