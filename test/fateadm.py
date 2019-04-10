# -*- coding: utf-8 -*-

import base64
import hashlib
import json
import time

import requests


class FateadmAPI():
    def __init__(self, app_id, app_key, usr_id, usr_key):
        self.app_id = app_id
        self.app_key = app_key
        self.usr_id = usr_id
        self.usr_key = usr_key
        self.host = 'http://pred.fateadm.com'

    def calc_sign(self, usr_id, passwd, timestamp):
        md5 = hashlib.md5()
        md5.update((timestamp + passwd).encode())
        csign = md5.hexdigest()

        md5 = hashlib.md5()
        md5.update((usr_id + timestamp + csign).encode())
        csign = md5.hexdigest()
        return csign

    # 识别验证码
    def predict(self, pred_type, img_data):
        tm = str(int(time.time()))

        param = {
            'user_id': self.usr_id,
            'timestamp': tm,
            'sign': self.calc_sign(self.usr_id, self.usr_key, tm),
            'predict_type': pred_type,
            'img_data': base64.b64encode(img_data),
        }

        if self.app_id != '':
            asign = self.calc_sign(self.app_id, self.app_key, tm)
            param['appid'] = self.app_id
            param['asign'] = asign

        r = requests.post('{}/api/capreg'.format(self.host), param)
        try:
            data = r.json()
            return json.loads(data['RspData'])['result']
        except Exception:
            raise Exception(r.text)
