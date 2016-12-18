ci_environment = False
try:
    import sys

    if sys.argv[1] == 'true':
        print('ci environment.')
        ci_environment = True
        username = sys.argv[2]
        password = sys.argv[3]
        soft_id = sys.argv[4]
        soft_key = sys.argv[5]
except IndexError:
    if not ci_environment:
        try:
            import config

            if config.soft_key:
                print('local environment')
                username = config.username
                password = config.password
                soft_id = config.soft_id
                soft_key = config.soft_key
        except ImportError:
            raise Exception('This is not ci or local environment.Please read README.md')
