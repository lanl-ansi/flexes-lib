import setuptools

with open('README.rst') as f:
    long_description = f.read()

setuptools.setup(
    name='flexes_lib',
    version='0.1.0',
    author='James Arnold',
    description='Helper library for interacting with flexes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[
        'boto3>=1.9.94',
        'ujson>=1.35'
        'aiohttp>=3.2.1',
        'requests>=2.18.4'
    ],
    extras_require={
        'dev': [
            'codecov',
            'mock',
            'pytest>=3.6',
            'pytest-mock'
        ]    
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent'
    ]
)
