# -*- coding: utf-8 -*-

import unittest

from nose.tools import assert_raises, assert_equal
from lxml import etree

from wechatsogou.tools import list_or_empty, get_elem_text, replace_html, str_to_dict, replace_space, get_url_param


class TestTools(unittest.TestCase):
    def test_list_or_empty(self):
        with assert_raises(AssertionError):
            list_or_empty('test for fun')

        assert_equal(list_or_empty(['1', '2'], int), 1)
        assert_equal(list_or_empty(['1', '2']), '1')
        assert_equal(list_or_empty([], int), 0)
        assert_equal(list_or_empty([], str), '')
        assert_equal(list_or_empty([], list), [])

    def test_get_elem_text(self):
        html = '''
        <div>
            <div>111</div>
            <div>222</div>
        </div>
        '''
        elem = etree.HTML(html)
        assert_equal(get_elem_text(elem), '111222')

    def test_replace_html(self):
        html = '''&#39;&quot;&amp;&yen;amp;&lt;&gt;&nbsp;\\'''
        assert_equal(replace_html(html), '\'"&¥<> ')

        html = ['&#39;', '&quot;', '&amp;', '&yen;', 'amp;', '&lt;', '&gt;', '&nbsp;', '\\']
        assert_equal(replace_html(html), ['\'', '"', '&', '¥', '', '<', '>', ' ', ''])

        html = {'&#39;': '&quot;'}
        assert_equal(replace_html(html), {'\'': '"'})

    def test_str_to_dict(self):
        string = "{'a':'a'}"
        assert_equal(str_to_dict(string), {'a': 'a'})

    def test_replace_space(self):
        string = 'ss ss'
        assert_equal(replace_space(string), 'ssss')

    def test_get_url_param(self):
        url = 'http://example.com?a=1&b=2&a=3'
        assert_equal(get_url_param(url), {'a': ['1', '3'], 'b': ['2']})


if __name__ == '__main__':
    unittest.main()
