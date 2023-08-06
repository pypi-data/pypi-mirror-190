#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="knoxnl",
    packages=find_packages(),
    version=__import__('knoxnl').__version__,
    description="A python wrapper around the amazing KNOXSS API by Brute Logic (requires an API Key)",
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',
    author="@xnl-h4ck3r",
    url="https://github.com/xnl-h4ck3r/knoxnl",
    py_modules=["knoxnl"],
    install_requires=["argparse","requests","termcolor"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'knoxnl = knoxnl:main'
        ]
    },
    keywords=['knoxnl', 'bug bounty', 'knoxss', 'xss', 'brutelogic', 'pentesting', 'security'],
)
