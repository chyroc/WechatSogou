# -*- coding: utf-8 -*-

import json

def prdict(content):
    msg = json.dumps(content, indent=1, ensure_ascii=False)
    print(msg)