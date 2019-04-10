# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import json
import re

import requests
from bs4 import BeautifulSoup
from lxml import etree
from lxml.etree import XML

from wechatsogou.exceptions import WechatSogouException
from wechatsogou.five import str_to_bytes
from wechatsogou.tools import get_elem_text, list_or_empty, replace_html, get_first_of_element, format_image_url

backgroud_image_p = re.compile('background-image:[ ]+url\(\"([\w\W]+?)\"\)')
js_content = re.compile('js_content.*?>((\s|\S)+)</div>')
find_article_json_re = re.compile('var msgList = (.*?)}}]};')
get_post_view_perm = re.compile('<script>var account_anti_url = "(.*?)";</script>')


class WechatSogouStructuring(object):
    @staticmethod
    def __handle_content_url(content_url):
        content_url = replace_html(content_url)
        return ('http://mp.weixin.qq.com{}'.format(
            content_url) if 'http://mp.weixin.qq.com' not in content_url else content_url) if content_url else ''

    @staticmethod
    def __get_post_view_perm(text):
        result = get_post_view_perm.findall(text)
        if not result or len(result) < 1 or not result[0]:
            return None

        r = requests.get('http://weixin.sogou.com{}'.format(result[0]))
        if not r.ok:
            return None

        if r.json().get('code') != 'success':
            return None

        return r.json().get('msg')

    @staticmethod
    def get_gzh_by_search(text):
        """从搜索公众号获得的文本 提取公众号信息

        Parameters
        ----------
        text : str or unicode
            搜索公众号获得的文本

        Returns
        -------
        list[dict]
            {
                'open_id': '', # 微信号唯一ID
                'profile_url': '',  # 最近10条群发页链接
                'headimage': '',  # 头像
                'wechat_name': '',  # 名称
                'wechat_id': '',  # 微信id
                'post_perm': '',  # 最近一月群发数
                'view_perm': '',  # 最近一月阅读量
                'qrcode': '',  # 二维码
                'introduction': '',  # 介绍
                'authentication': ''  # 认证
            }
        """
        post_view_perms = WechatSogouStructuring.__get_post_view_perm(text)

        page = etree.HTML(text)
        lis = page.xpath('//ul[@class="news-list2"]/li')
        relist = []
        for li in lis:
            url = get_first_of_element(li, 'div/div[1]/a/@href')
            headimage = format_image_url(get_first_of_element(li, 'div/div[1]/a/img/@src'))
            wechat_name = get_elem_text(get_first_of_element(li, 'div/div[2]/p[1]'))
            info = get_elem_text(get_first_of_element(li, 'div/div[2]/p[2]'))
            qrcode = get_first_of_element(li, 'div/div[3]/span/img[1]/@src')
            introduction = get_elem_text(get_first_of_element(li, 'dl[1]/dd'))
            authentication = get_first_of_element(li, 'dl[2]/dd/text()')

            relist.append({
                'open_id': headimage.split('/')[-1],
                'profile_url': url,
                'headimage': headimage,
                'wechat_name': wechat_name.replace('red_beg', '').replace('red_end', ''),
                'wechat_id': info.replace('微信号：', ''),
                'qrcode': qrcode,
                'introduction': introduction.replace('red_beg', '').replace('red_end', ''),
                'authentication': authentication,
                'post_perm': -1,
                'view_perm': -1,
            })

        if post_view_perms:
            for i in relist:
                if i['open_id'] in post_view_perms:
                    post_view_perm = post_view_perms[i['open_id']].split(',')
                    if len(post_view_perm) == 2:
                        i['post_perm'] = int(post_view_perm[0])
                        i['view_perm'] = int(post_view_perm[1])
        return relist

    @staticmethod
    def get_article_by_search_wap(keyword, wap_dict):
        datas = []
        for i in wap_dict['items']:
            item = str_to_bytes(i).replace(b'\xee\x90\x8a' + str_to_bytes(keyword) + b'\xee\x90\x8b',
                                           str_to_bytes(keyword))
            root = XML(item)
            display = root.find('.//display')
            datas.append({
                'gzh': {
                    'profile_url': display.find('encGzhUrl').text,
                    'open_id': display.find('openid').text,
                    'isv': display.find('isV').text,
                    'wechat_name': display.find('sourcename').text,
                    'wechat_id': display.find('username').text,
                    'headimage': display.find('headimage').text,
                    'qrcode': display.find('encQrcodeUrl').text,
                },
                'article': {
                    'title': display.find('title').text,
                    'url': display.find('url').text,  # encArticleUrl
                    'main_img': display.find('imglink').text,
                    'abstract': display.find('content168').text,
                    'time': display.find('lastModified').text,
                },
            })

        return datas

    @staticmethod
    def get_article_by_search(text):
        """从搜索文章获得的文本 提取章列表信息

        Parameters
        ----------
        text : str or unicode
            搜索文章获得的文本

        Returns
        -------
        list[dict]
            {
                'article': {
                    'title': '',  # 文章标题
                    'url': '',  # 文章链接
                    'imgs': '',  # 文章图片list
                    'abstract': '',  # 文章摘要
                    'time': ''  # 文章推送时间
                },
                'gzh': {
                    'profile_url': '',  # 公众号最近10条群发页链接
                    'headimage': '',  # 头像
                    'wechat_name': '',  # 名称
                    'isv': '',  # 是否加v
                }
            }
        """
        page = etree.HTML(text)
        lis = page.xpath('//ul[@class="news-list"]/li')

        articles = []
        for li in lis:
            url = get_first_of_element(li, 'div[1]/a/@href')
            if url:
                title = get_first_of_element(li, 'div[2]/h3/a')
                imgs = li.xpath('div[1]/a/img/@src')
                abstract = get_first_of_element(li, 'div[2]/p')
                time = get_first_of_element(li, 'div[2]/div/span/script/text()')
                gzh_info = li.xpath('div[2]/div/a')[0]
            else:
                url = get_first_of_element(li, 'div/h3/a/@href')
                title = get_first_of_element(li, 'div/h3/a')
                imgs = []
                spans = li.xpath('div/div[1]/a')
                for span in spans:
                    img = span.xpath('span/img/@src')
                    if img:
                        imgs.append(img)
                abstract = get_first_of_element(li, 'div/p')
                time = get_first_of_element(li, 'div/div[2]/span/script/text()')
                gzh_info = li.xpath('div/div[2]/a')[0]

            if title is not None:
                title = get_elem_text(title).replace("red_beg", "").replace("red_end", "")
            if abstract is not None:
                abstract = get_elem_text(abstract).replace("red_beg", "").replace("red_end", "")

            time = re.findall('timeConvert\(\'(.*?)\'\)', time)
            time = list_or_empty(time, int)
            profile_url = get_first_of_element(gzh_info, '@href')
            headimage = get_first_of_element(gzh_info, '@data-headimage')
            wechat_name = get_first_of_element(gzh_info, 'text()')
            gzh_isv = get_first_of_element(gzh_info, '@data-isv', int)

            articles.append({
                'article': {
                    'title': title,
                    'url': url,
                    'imgs': format_image_url(imgs),
                    'abstract': abstract,
                    'time': time
                },
                'gzh': {
                    'profile_url': profile_url,
                    'headimage': headimage,
                    'wechat_name': wechat_name,
                    'isv': gzh_isv,
                }
            })
        return articles

    @staticmethod
    def get_gzh_info_by_history(text):
        """从 历史消息页的文本 提取公众号信息

        Parameters
        ----------
        text : str or unicode
            历史消息页的文本

        Returns
        -------
        dict
            {
                'wechat_name': '',  # 名称
                'wechat_id': '',  # 微信id
                'introduction': '',  # 描述
                'authentication': '',  # 认证
                'headimage': ''  # 头像
            }
        """

        page = etree.HTML(text)
        profile_area = get_first_of_element(page, '//div[@class="profile_info_area"]')

        profile_img = get_first_of_element(profile_area, 'div[1]/span/img/@src')
        profile_name = get_first_of_element(profile_area, 'div[1]/div/strong/text()')
        profile_wechat_id = get_first_of_element(profile_area, 'div[1]/div/p/text()')
        profile_desc = get_first_of_element(profile_area, 'ul/li[1]/div/text()')
        profile_principal = get_first_of_element(profile_area, 'ul/li[2]/div/text()')

        return {
            'wechat_name': profile_name.strip(),
            'wechat_id': profile_wechat_id.replace('微信号: ', '').strip('\n'),
            'introduction': profile_desc,
            'authentication': profile_principal,
            'headimage': profile_img
        }

    @staticmethod
    def get_article_by_history_json(text, article_json=None):
        """从 历史消息页的文本 提取文章列表信息

        Parameters
        ----------
        text : str or unicode
            历史消息页的文本
        article_json : dict
            历史消息页的文本 提取出来的文章json dict

        Returns
        -------
        list[dict]
            {
                'send_id': '',  # 群发id，注意不唯一，因为同一次群发多个消息，而群发id一致
                'datetime': '',  # 群发datatime
                'type': '',  # 消息类型，均是49，表示图文
                'main': 0,  # 是否是一次群发的第一次消息
                'title': '',  # 文章标题
                'abstract': '',  # 摘要
                'fileid': '',  #
                'content_url': '',  # 文章链接
                'source_url': '',  # 阅读原文的链接
                'cover': '',  # 封面图
                'author': '',  # 作者
                'copyright_stat': '',  # 文章类型，例如：原创啊
            }

        """
        if article_json is None:
            article_json = find_article_json_re.findall(text)
            if not article_json:
                return []
            article_json = article_json[0] + '}}]}'
            article_json = json.loads(article_json)

        items = list()

        for listdic in article_json['list']:
            if str(listdic['comm_msg_info'].get('type', '')) != '49':
                continue

            comm_msg_info = listdic['comm_msg_info']
            app_msg_ext_info = listdic['app_msg_ext_info']
            send_id = comm_msg_info.get('id', '')
            msg_datetime = comm_msg_info.get('datetime', '')
            msg_type = str(comm_msg_info.get('type', ''))

            items.append({
                'send_id': send_id,
                'datetime': msg_datetime,
                'type': msg_type,
                'main': 1, 'title': app_msg_ext_info.get('title', ''),
                'abstract': app_msg_ext_info.get('digest', ''),
                'fileid': app_msg_ext_info.get('fileid', ''),
                'content_url': WechatSogouStructuring.__handle_content_url(app_msg_ext_info.get('content_url')),
                'source_url': app_msg_ext_info.get('source_url', ''),
                'cover': app_msg_ext_info.get('cover', ''),
                'author': app_msg_ext_info.get('author', ''),
                'copyright_stat': app_msg_ext_info.get('copyright_stat', '')
            })

            if app_msg_ext_info.get('is_multi', 0) == 1:
                for multi_dict in app_msg_ext_info['multi_app_msg_item_list']:
                    items.append({
                        'send_id': send_id,
                        'datetime': msg_datetime,
                        'type': msg_type,
                        'main': 0, 'title': multi_dict.get('title', ''),
                        'abstract': multi_dict.get('digest', ''),
                        'fileid': multi_dict.get('fileid', ''),
                        'content_url': WechatSogouStructuring.__handle_content_url(multi_dict.get('content_url')),
                        'source_url': multi_dict.get('source_url', ''),
                        'cover': multi_dict.get('cover', ''),
                        'author': multi_dict.get('author', ''),
                        'copyright_stat': multi_dict.get('copyright_stat', '')
                    })

        return list(filter(lambda x: x['content_url'], items))  # 删除搜狗本身携带的空数据

    @staticmethod
    def get_gzh_info_and_article_by_history(text):
        """从 历史消息页的文本 提取公众号信息 和 文章列表信息

        Parameters
        ----------
        text : str or unicode
            历史消息页的文本

        Returns
        -------
        dict
            {
                'gzh': {
                    'wechat_name': '',  # 名称
                    'wechat_id': '',  # 微信id
                    'introduction': '',  # 描述
                    'authentication': '',  # 认证
                    'headimage': ''  # 头像
                },
                'article': [
                    {
                        'send_id': '',  # 群发id，注意不唯一，因为同一次群发多个消息，而群发id一致
                        'datetime': '',  # 群发datatime
                        'type': '',  # 消息类型，均是49，表示图文
                        'main': 0,  # 是否是一次群发的第一次消息
                        'title': '',  # 文章标题
                        'abstract': '',  # 摘要
                        'fileid': '',  #
                        'content_url': '',  # 文章链接
                        'source_url': '',  # 阅读原文的链接
                        'cover': '',  # 封面图
                        'author': '',  # 作者
                        'copyright_stat': '',  # 文章类型，例如：原创啊
                    },
                    ...
                ]
            }
        """
        return {
            'gzh': WechatSogouStructuring.get_gzh_info_by_history(text),
            'article': WechatSogouStructuring.get_article_by_history_json(text)
        }

    @staticmethod
    def get_gzh_article_by_hot(text):
        """从 首页热门搜索 提取公众号信息 和 文章列表信息

        Parameters
        ----------
        text : str or unicode
            首页热门搜索 页 中 某一页 的文本

        Returns
        -------
        list[dict]
            {
                'gzh': {
                    'headimage': str,  # 公众号头像
                    'wechat_name': str,  # 公众号名称
                },
                'article': {
                    'url': str,  # 文章临时链接
                    'title': str,  # 文章标题
                    'abstract': str,  # 文章摘要
                    'time': int,  # 推送时间，10位时间戳
                    'open_id': str,  # open id
                    'main_img': str  # 封面图片
                }
            }
        """
        page = etree.HTML(text)
        lis = page.xpath('/html/body/li')
        gzh_article_list = []
        for li in lis:
            url = get_first_of_element(li, 'div[1]/h4/a/@href')
            title = get_first_of_element(li, 'div[1]/h4/a/div/text()')
            abstract = get_first_of_element(li, 'div[1]/p[1]/text()')
            xpath_time = get_first_of_element(li, 'div[1]/p[2]')
            open_id = get_first_of_element(xpath_time, 'span/@data-openid')
            headimage = get_first_of_element(xpath_time, 'span/@data-headimage')
            gzh_name = get_first_of_element(xpath_time, 'span/text()')
            send_time = xpath_time.xpath('a/span/@data-lastmodified')
            main_img = get_first_of_element(li, 'div[2]/a/img/@src')

            try:
                send_time = int(send_time[0])
            except ValueError:
                send_time = send_time[0]

            gzh_article_list.append({
                'gzh': {
                    'headimage': headimage,
                    'wechat_name': gzh_name,
                },
                'article': {
                    'url': url,
                    'title': title,
                    'abstract': abstract,
                    'time': send_time,
                    'open_id': open_id,
                    'main_img': main_img
                }
            })

        return gzh_article_list

    @staticmethod
    def get_article_detail(text, del_qqmusic=True, del_voice=True):
        """根据微信文章的临时链接获取明细

        1. 获取文本中所有的图片链接列表
        2. 获取微信文章的html内容页面(去除标题等信息)

        Parameters
        ----------
        text : str or unicode
            一篇微信文章的文本
        del_qqmusic: bool
            删除文章中的qq音乐
        del_voice: bool
            删除文章中的语音内容

        Returns
        -------
        dict
        {
            'content_html': str # 微信文本内容
            'content_img_list': list[img_url1, img_url2, ...] # 微信文本中图片列表

        }
        """
        # 1. 获取微信文本content
        html_obj = BeautifulSoup(text, "lxml")
        content_text = html_obj.find('div', {'class': 'rich_media_content', 'id': 'js_content'})

        # 2. 删除部分标签
        if del_qqmusic:
            qqmusic = content_text.find_all('qqmusic') or []
            for music in qqmusic:
                music.parent.decompose()

        if del_voice:
            # voice是一个p标签下的mpvoice标签以及class为'js_audio_frame db'的span构成，所以将父标签删除
            voices = content_text.find_all('mpvoice') or []
            for voice in voices:
                voice.parent.decompose()

        # 3. 获取所有的图片 [img标签，和style中的background-image]
        all_img_set = set()
        all_img_element = content_text.find_all('img') or []
        for ele in all_img_element:
            # 删除部分属性
            img_url = format_image_url(ele.attrs['data-src'])
            del ele.attrs['data-src']

            ele.attrs['src'] = img_url

            if not img_url.startswith('http'):
                raise WechatSogouException('img_url [{}] 不合法'.format(img_url))
            all_img_set.add(img_url)

        backgroud_image = content_text.find_all(style=re.compile("background-image")) or []
        for ele in backgroud_image:
            # 删除部分属性
            if ele.attrs.get('data-src'):
                del ele.attrs['data-src']

            if ele.attrs.get('data-wxurl'):
                del ele.attrs['data-wxurl']
            img_url = re.findall(backgroud_image_p, str(ele))
            if not img_url:
                continue
            all_img_set.add(img_url[0])

        # 4. 处理iframe
        all_img_element = content_text.find_all('iframe') or []
        for ele in all_img_element:
            # 删除部分属性
            img_url = ele.attrs['data-src']
            del ele.attrs['data-src']
            ele.attrs['src'] = img_url

        # 5. 返回数据
        all_img_list = list(all_img_set)
        content_html = content_text.prettify()
        # 去除div[id=js_content]
        content_html = re.findall(js_content, content_html)[0][0]
        return {
            'content_html': content_html,
            'content_img_list': all_img_list
        }
