#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Vin on 2017/7/28

import time
import requests
from keras.applications.xception import Xception, preprocess_input
from keras.models import model_from_json
import numpy as np
from scipy import misc


def load_model():
    # load json and create model
    json_file = open('model.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights("model.h5")
    print("Loaded model from disk")
    # loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
    loaded_model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return loaded_model


def get_captcha():
    _headers = {
        'Host': 'mp.weixin.qq.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.14 Safari/537.36',
    }
    time_str = str(time.time()).replace('.', '')
    timestamp = time_str[0:13] + '.' + time_str[13:17]
    url = 'http://mp.weixin.qq.com/mp/verifycode?cert=' + timestamp
    try:
        captcha = requests.get(url=url, headers=_headers)
        img_name = '/mnt/e/ubuntu/captcha.jpg'
        with open(img_name, 'wb') as fp:
            fp.write(captcha.content)
        return img_name
    except requests.RequestException:
        return None


def deal_captcha(captcha=None):
    if captcha is None:
        return False
    img_size = (50, 120)
    x = [misc.imresize(misc.imread(captcha), img_size)]
    x = preprocess_input(np.array(x).astype(float))
    return x


if __name__ == '__main__':
    model = load_model()
    captcha = get_captcha()
    input_img = deal_captcha(captcha)
    result = model.predict(input_img)
    result = np.array([i.argmax(axis=1) for i in result]).T
    code_list = []
    for code in result:
        temp = []
        for word_offset in code:
            word = chr(ord('a') + word_offset)
            temp.append(word)
        code_list.append(temp)
    print(code_list)