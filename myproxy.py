import requests
import re
import random

def get():
    retu = list()
    r = requests.get('http://proxy.goubanjia.com/free/gngn/index.shtml')
    ips = re.findall(r'<td class="ip">(.*?)</td>', r.text)
    ips = [re.compile(r'<[^>]+>', re.S).sub('', ip) for ip in ips]
    print(ips)
    exit()
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
    pros = get()
    while True:
        pro = pros[random.randint(0, len(pros) - 1)]
        if test(pro):
            return pro

if __name__ == '__main__':
    get()