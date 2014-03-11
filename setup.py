import os
import sys

from setuptools import find_packages, setup

setup(
    name = 'RPiCar',
    version = '0.0.1',
    description = 'Raspberry Pi car lib',
    keywords = 'Raspberry Pi car',
    url = 'https://github.com/zhouyougit/RPiCar',
    author = 'zhouyou',
    author_email = 'zhouyoug@gmail.com',
    packages = find_packages(exclude = ['*.pyc'])
)
