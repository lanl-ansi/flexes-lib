import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='lanlytics_api_lib',
    version='1.0.0',
    author='James Arnold',
    description='Helper library for interacting with the lanlytics API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp>=3.2.1',
        'requests>=2.18.4'
    ],
    extras_require={
        'dev': [
            'codecov',
            'pytest',
            'pytest-cov',
            'pytest-mock'
        ]    
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent'
    ]
)
