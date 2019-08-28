import codecs
import re

from setuptools import setup

readme = codecs.open('docs/README.rst', encoding='utf-8').read()
history = codecs.open('docs/HISTORY.rst', encoding='utf-8').read()
with codecs.open("wechatsogou/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='wechatsogou',
    version=version,
    description='Api for wechat mp with sogou',
    long_description=u'\n\n'.join([readme, history]),
    author='Chyroc',
    author_email='chen_yunpeng@foxmail.com',
    url='https://github.com/Chyroc/WechatSogou',
    packages=[
        'wechatsogou',
    ],
    setup_requires=[
        # minimum version to use environment markers
        'setuptools>=20.6.8',
    ],
    install_requires=[
        'future', 'lxml', 'Pillow', 'requests', 'six', 'Werkzeug', 'xlrd', 'bs4'
    ],
    include_package_data=True,
    license='MIT License',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
