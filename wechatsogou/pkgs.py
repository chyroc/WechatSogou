# -*- coding: utf-8 -*-

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
