import unittest

from wechatsogou import RClient
from test import env_variable


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
