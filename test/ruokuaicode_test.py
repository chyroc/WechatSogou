import unittest

from test import config
from wechatsogou.ruokuaicode import RClient


class RuokuaicodeTest(unittest.TestCase):
    def test_create(self):
        rc = RClient(config.username, config.password, config.soft_id, config.soft_key)
        with open('code.jpg', 'rb') as f:
            im = f.read()
        result = rc.create(im, '3060')
        result_str = result['Result'].lower()
        assert result_str == '61xmv3'


if __name__ == '__main__':
    unittest.main()
