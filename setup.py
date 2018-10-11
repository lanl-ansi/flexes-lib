import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='aws_utils',
    version='0.1.0',
    author='James Arnold',
    description='Utilities for interacting with Amazon Web Services',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[
        'boto3>=1.7.17',
        'ujson>=1.35'
    ],
    extras_require={
        'dev': [
            'codecov',
            'mock',
            'pytest',
            'pytest-cov'
        ]    
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent'
    ]
)
