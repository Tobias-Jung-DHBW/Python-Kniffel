"""
the setup module is used to prepare kniffel for a pip install
"""
import sys
from setuptools import setup
from setuptools import find_packages

INSTALL_REQUIRES = ["numpy"]

if sys.platform.startswith('win'):
    INSTALL_REQUIRES.append("windows-curses")

setup(
    name="kniffel",
    version="1.0.0",
    description="A small kniffel emulator",
    packages=find_packages(where='kniffel'),
    install_requires=INSTALL_REQUIRES,
    package_dir={
        '': 'kniffel',
    }
)
