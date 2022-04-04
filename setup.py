import os
import sys
import platform
import shutil
from setuptools import setup, find_packages

setup(
    name="loganalyzer",
    version='1.1',
    description='Python Script for parsing and analyzing agent2D socer simulation rcl and rcg logs',
    long_description=open("README.md").read(),
    author='Shahryar Bhm & Farzin Negahbani',
    author_email='shahryarbahmeie@gmail.com , farzin.negahbani@gmail.comh',
    url='https://github.com/Farzin-Negahbani/Namira_LogAnalyzer',
    packages=find_packages(),
    install_requires = ['pandas'],
    scripts = [
            'scripts/loganalyzer',
    ],
)