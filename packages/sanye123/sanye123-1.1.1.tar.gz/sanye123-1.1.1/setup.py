#!/usr/bin/env python
from io import open
from setuptools import setup, find_packages
setup(
    name='sanye123',
    version='1.1.1',
    description='a package for your bert using',
    long_description='使用keras实现你的bert项目',
    author='sanye',
    author_email='201419490@qq.com',
    license='Apache License 2.0',
    url='https://github.com/boss2020/tfbert',
    download_url='https://github.com/boss2020/tfbert/master.zip',
    packages=find_packages(),
    install_requires=['tensorflow>=2.4.0rc0']
)