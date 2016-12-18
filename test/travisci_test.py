



try:
    print(1)
    print(ruokuai_name)
except Exception as e:
    print(e)

try:
    print(2)
    import sys
    print(sys.argv)
except Exception as e:
    print(e)


try:
    print(3)
    import System
    System.getenv()
except Exception as e:
    print(e)


try:
    print(4)
    import os
    os.environ['']
    os.environ.get('ruokuai_name')
except Exception as e:
    print(e)