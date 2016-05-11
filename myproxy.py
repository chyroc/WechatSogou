import requests
import re
import random

def get(nei='http'):
    retu = list()
    r = requests.get('http://ip84.com/dlgn-http')
    myItems = re.findall('<tr>(.+?)<td>(.+?)</td>(.+?)<td>(.+?)</td>(.+?)<td>(.+?)</td>(.+?)<td>(.+?)</td>(.+?)<td>(.+?)</td>(.+?)<td>(.+?)</td>(.+?)<td>(.+?)</td>(.+?)</tr>', r.text, re.S)
    for items in myItems:
        if items[9].lower() == nei:
            retu.append({'ip':items[1], 'duan':items[3], 'http':items[9].lower()})
    return retu
def test(pro):
    proxies = {
        pro['http']: "http://"+pro['ip']+":"+pro['duan']
    }
    try:
        requests.get("http://baidu.com", proxies=proxies, timeout=5)
    except:
        return False
    else:
        return True
def get_one(nei='http'):
    pros = get(nei)
    while True:
        pro = pros[random.randint(0, len(pros) - 1)]
        if test(pro):
            return pro