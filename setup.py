# -*- coding: utf-8 -*-
 
 
from __future__ import with_statement
 
import sys
if sys.version_info < (2, 5):
    sys.exit('Python 2.5 or greater is required.')
 
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
 
import wechatsogou

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()
 
setup(name='wechatsogou',
      version=wechatsogou.__version__,
      description='api for wechat mp with sogou.',
      long_description=read_md('README.md'),
      author='Chyroc Chen',
      author_email='chen_yunpeng@foxmail.com',
      keywords='python web wechat sogou requests',
      url='https://github.com/Chyroc/WechatSogou',
      include_package_data=True,
      packages=['wechatsogou'],
      license=license,
      platforms=['any'],
      classifiers=[]
      )