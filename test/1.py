import unittest

from test import env_variable
from wechatsogou.ruokuaicode import RClient



s = env_variable
rc = RClient(env_variable.username, env_variable.password, env_variable.soft_id, env_variable.soft_key)
with open('code.jpg', 'rb') as f:
    im = f.read()
result = rc.create(im, '3060')
result_str = result['Result'].lower()
assert result_str == '61xmv3'


