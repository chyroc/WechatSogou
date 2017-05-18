import unittest
from nose.tools import assert_raises, assert_equal

from wechatsogou.tools import (
    list_or_empty
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


if __name__ == '__main__':
    unittest.main()
