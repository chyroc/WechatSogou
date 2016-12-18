import sys
import unittest

sys.path.append('../')
import env_variable
from ..wechatsogou import RClient


class RuokuaicodeTest(unittest.TestCase):
    def test_create(self):
        rc = RClient(env_variable.username, env_variable.password, env_variable.soft_id, env_variable.soft_key)
        with open('code.jpg', 'rb') as f:
            im = f.read()
        result = rc.create(im, '3060')
        result_str = result['Result'].lower()
        assert result_str == '61xmv3'


if __name__ == '__main__':
    unittest.main()
