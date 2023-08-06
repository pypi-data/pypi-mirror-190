#!/usr/bin/env python
from io import open
from setuptools import setup, find_packages
from __version__ import __version__
setup(
    name='fastposter',
    version=__version__,
    description='a package for fastposter cloud client',
    long_description='fastposter-cloud python客户端，轻松开发海报。https://cloud.fastposter.net/',
    author='Alex',
    author_email='service@fastposter.net',
    license='MIT License',
    url='https://github.com/psoho/fastposter-cloud-client-python',
    download_url='https://github.com/psoho/fastposter-cloud-client-python/main.zip',
    packages=find_packages(),
    install_requires=['requests==2.28.2']
)
