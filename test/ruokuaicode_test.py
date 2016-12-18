import unittest

import env_variable
from wechatsogou import RClient


class RuokuaicodeTest(unittest.TestCase):
    def test_create(self):
        s = env_variable
        rc = RClient(env_variable.username, env_variable.password, env_variable.soft_id, env_variable.soft_key)
        with open('code.jpg', 'rb') as f:
            im = f.read()
        result = rc.create(im, '3060')
        result_str = result['Result'].lower()
        assert result_str == '61xmv3'


if __name__ == '__main__':
    unittest.main()
