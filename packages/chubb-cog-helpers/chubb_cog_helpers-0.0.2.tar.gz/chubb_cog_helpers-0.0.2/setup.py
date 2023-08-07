import os, pathlib
from setuptools import setup, find_packages
from subprocess import check_call

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

setup(
    name = 'chubb_cog_helpers', 
    version = '0.0.2', 
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ], 
    url = 'https://www.chubb.com/us-en/', 
    author = 'Nicholas Ciesla (Chubb)',  
    author_email = 'nicholas.ciesla@chubb.com', 
    description = 'Helper functions for Chubb COG',
    long_description = LONG_DESCRIPTION,
    long_description_content_type = 'text/markdown',
    packages = find_packages(),   
    py_modules = ['chubb_cog_helpers.secret_locker',
                  'chubb_cog_helpers.metrics'],     
    python_requires = '>=3.8',
    install_requires = []
)