import sys

if sys.argv[1] == 'true':
    print('ci env')


from test import config
if config.soft_key:
    print('local env')