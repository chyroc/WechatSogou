import unittest
from nose.tools import assert_raises, assert_equal

from lxml import etree
from wechatsogou.tools import (
    list_or_empty,
    get_elem_text,
    _replace_html
)


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
        assert_equal(_replace_html(html), '\'"&¥<> ')


if __name__ == '__main__':
    unittest.main()
