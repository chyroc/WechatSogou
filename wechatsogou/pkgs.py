# -*- coding: utf-8 -*-

from PIL import Image

# url_parse
try:
    import urlparse as url_parse
except ImportError:
    import urllib.parse as url_parse

# urlencode
try:
    from urllib import urlencode
    import sys

    reload(sys)
    sys.setdefaultencoding('utf-8')
except ImportError:
    import urllib.parse

    urlencode = urllib.parse.urlencode

# unquote
try:
    from urllib import unquote
except:
    from urllib.parse import unquote

# quote
try:
    from urllib.request import quote as quote
except ImportError:
    from urllib import quote as quote

# readimg
try:
    import StringIO

    def readimg(content):
        return Image.open(StringIO.StringIO(content))
except ImportError:
    import tempfile

    def readimg(content):
        f = tempfile.TemporaryFile()
        f.write(content)
        return Image.open(f)

try:
    input = raw_input
except NameError:
    input = input
