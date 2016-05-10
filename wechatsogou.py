#coding=utf-8

from lxml import etree
import requests
import re

def get_elem_text(elem):
    rc = []
    for node in elem.itertext():
        rc.append(node.strip())
    return ''.join(rc)

def get_encoding_from_reponse(r):
    encoding = requests.utils.get_encodings_from_content(r.text)
    if encoding:
        return encoding[0]
    else:
        return requests.utils.get_encoding_from_headers(r.headers)
def _get(url, host=''):
    headers = {
        "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454.101 Chrome/45.0.2454.101 Safari/537.36',
        "Referer": 'http://weixin.sogou.com/',
        'Host': host if host else 'weixin.sogou.com',
    }
    # pro = proxy.run_one()
    # proxies = {
    #     pro['http']: "http://" + pro['ip'] + ":" + pro['duan']
    # }
    # print(proxies)
    r = requests.get(url, headers=headers)  # , proxies=proxies
    if r.status_code == requests.codes.ok:
        r.encoding = get_encoding_from_reponse(r)
        if '需要您协助验证' in r.text:
            raise Exception('http get Verification code')
    else:
        raise Exception('requests status_code error')
    return r.text
def replace_html(s):
    s = s.replace('&quot;','"')
    s = s.replace('&amp;','&')
    s = s.replace('amp;','')
    s = s.replace('&lt;','<')
    s = s.replace('&gt;','>')
    s = s.replace('&nbsp;',' ')
    s = s.replace(r"\\", r'')
    return s
def _search_gzh(name, page=1):
    request_url = 'http://weixin.sogou.com/weixin?query='+name+'&_sug_type_=&_sug_=n&type=1&page='+str(page)+'&ie=utf8'
    try:
        text = _get(request_url)
        return text
    except Exception as e:
        print(e)
        return False

def search_gzh_info(name, page):
    text = _search_gzh(name, page)
    page = etree.HTML(text)

    info_imgs = page.xpath(u"//div[@class='img-box']/img")
    img = list()
    for info_img in info_imgs:
        img.append(info_img.attrib['src'])

    info_urls = page.xpath(u"//div[@target='_blank']")
    url = list()
    for info_url in info_urls:
        url.append(info_url.attrib['href'])

    name = list()
    wechatid = list()
    jieshao = list()
    renzhen = list()
    info_instructions = page.xpath(u"//div[@class='txt-box']")
    for info_instruction in info_instructions:
        cache = get_elem_text(info_instruction)
        cache = cache.replace('red_beg','')
        cache = cache.replace('red_end', '')
        cache_list = cache.split('\n')
        cache_re = re.split('微信号：|功能介绍：|认证：|最近文章：', cache_list[0])
        name.append(cache_re[0])
        wechatid.append(cache_re[1])
        if ".authnamewrite('2')" in cache_re[2]:
            jieshao.append(cache_re[2].replace(".authnamewrite('2')",''))
            renzhen.append(cache_re[3])
        else:
            jieshao.append(cache_re[2])
            renzhen.append('')

    qrcodes = list()
    info_qrcodes = page.xpath(u"//div[@class='pos-ico']/div/img")
    for info_qrcode in info_qrcodes:
        qrcodes.append(info_qrcode.attrib['src'])

    returns = list()
    for i in range(len(qrcodes)):
        returns.append(
            {'name':name[i],
             'wechatid':wechatid[i],
             'jieshao':jieshao[i],
             'renzhen':renzhen[i],
             'qrcode':qrcodes[i],
             'img':img[i],
             'url':url[i]
             }
        )
    return returns

def get_gzh_info(wechatid):
    info = search_gzh_info(wechatid, 1)
    if info:
        return info[0]
    else:
        return False

def get_gzh_article_dict(url):
    try:
        text = _get(url, 'mp.weixin.qq.com')
        print('dui')
    except Exception as e:
        print(e)
        exit()
    msglist = re.findall("var msgList = '(.+?)';", text, re.S)[0]
    msgdict = eval(replace_html(msglist))
    return msgdict

def get_gzh_article_detail(msgdict):
    """
    省略了list->comm_msg_info,list->app_msg_ext_info->(subtype)
    """
    items = list()
    for listdic in msgdict['list']:
        item = listdic['app_msg_ext_info']
        """copyright_stat解释
        100是普通
        11是原创
        101是转载
        """
        items.append(
            {'main':'1','title': item['title'], 'digest': item['digest'], 'content': item['content'], 'fileid': item['fileid'],
             'content_url': 'http://mp.weixin.qq.com' + item['content_url'], 'source_url': item['source_url'],
             'cover': item['cover'], 'author': item['author'], 'copyright_stat': item['copyright_stat']})
        if item['is_multi'] == 1:
            for multidic in item['multi_app_msg_item_list']:
                items.append({'main':'0','title': multidic['title'], 'digest': multidic['digest'], 'content': multidic['content'],
                              'fileid': multidic['fileid'],
                              'content_url': 'http://mp.weixin.qq.com' + multidic['content_url'],
                              'source_url': multidic['source_url'],
                              'cover': multidic['cover'], 'author': multidic['author'],
                              'copyright_stat': multidic['copyright_stat']})

    return items
