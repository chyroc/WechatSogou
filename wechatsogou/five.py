# -*- coding: utf-8 -*-

from PIL import Image
import six

if six.PY2:
    import sys
    import urlparse as url_parse
    from urllib import urlencode
    from urllib import unquote
    from urllib import quote as quote
    import StringIO

    def readimg(content):
        return Image.open(StringIO.StringIO(content))

    reload(sys)
    sys.setdefaultencoding('utf-8')
    input = raw_input
    str_to_bytes = bytes
else:
    import urllib.parse as url_parse
    import urllib.parse
    from urllib.parse import unquote
    from urllib.request import quote as quote
    import tempfile

    def readimg(content):
        f = tempfile.TemporaryFile()
        f.write(content)
        return Image.open(f)

    urlencode = urllib.parse.urlencode
    input = input
    str_to_bytes = lambda x: bytes(x, encoding='utf-8')
