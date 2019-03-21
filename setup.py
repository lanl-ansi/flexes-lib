import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='flexes_lib',
    version='0.1.1',
    author='James Arnold',
    description='Helper library for interacting with flexes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp>=3.2.1',
        'boto3>=1.9.94',
        'requests>=2.18.4',
        'ujson>=1.35'
    ],
    extras_require={
        'dev': [
            'codecov',
            'mock',
            'pytest>=3.6',
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
