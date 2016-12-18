# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from codecs import open
from os import path
import wechatsogou

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='wechatsogou',

    version=wechatsogou.__version__,

    description='api for wechat mp with sogou.',
    long_description=long_description,

    url='https://github.com/Chyroc/WechatSogou',

    author='Chyroc Chen',
    author_email='chen_yunpeng@foxmail.com',

    license='MIT',

    keywords='python web wechat sogou api weixin',

    packages=find_packages(),

    install_requires=['requests'],

    extras_require={},
)