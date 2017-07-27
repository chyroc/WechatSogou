基于搜狗微信搜索的微信公众号爬虫接口
===

[![Build Status](https://travis-ci.org/Chyroc/WechatSogou.svg?branch=master)](https://github.com/Chyroc/WechatSogou)
[![PyPI version](https://badge.fury.io/py/wechatsogou.svg)](https://github.com/Chyroc/WechatSogou)
[![PyPI](https://img.shields.io/pypi/wheel/wechatsogou.svg)](https://github.com/Chyroc/WechatSogou)
[![py27,py35,py36](https://img.shields.io/pypi/pyversions/wechatsogou.svg)](https://github.com/Chyroc/WechatSogou)
[![PyPI](https://img.shields.io/pypi/l/wechatsogou.svg)](https://github.com/Chyroc/WechatSogou)

# 项目简介
基于搜狗微信搜索的微信公众号爬虫接口，可以扩展成基于搜狗搜索的爬虫

如果有问题，请提issue

[CHANGELOG](./CHANGELOG.md)

# 交流QQ群
<a target="_blank" href="//shang.qq.com/wpa/qunwpa?idkey=2c888d2a84978b1fe863482166b9fe5e6418ae72eb2bf727905734d6af654fa5"><img border="0" src="http://pub.idqqimg.com/wpa/images/group.png" alt="Github搜狗微信爬虫交流" title="Github搜狗微信爬虫交流">132955136</a>

# 赞助作者
甲鱼说，咖啡是灵魂的饮料，买点咖啡

<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/pay_zfb.jpg" width="250" />
<img src="https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/pay_wx.jpg" width="250" />

谢谢：

- [微信] [ax4] [50]
- [微信] [风雨坛·君] [50]
- [支付宝] [陆小凤] [28.88]
- [支付宝] [朋鑫] [18.88]
- [微信] [JenkinsY94] [9.99]
- [微信] [谁认领一下] [8]
- [微信] [谁认领一下] [1]

# 问题集锦
    Q:没有得到原始文章url？
    A:微信屏蔽此接口，请在临时链接有效期内保存文章内容。

    Q:获取文章只能10篇？
    A:是的，仅显示最近10条群发。

    Q:使用的是python 2 还是 3？
    A:都支持，若出错，请报BUG。

## 安装

    pip install wechatsogou

## 日志

    import logging
    import logging.config
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()

## 引用

```python
import wechatsogou

wechats = wechatsogou.WechatSogouAPI()
```

## 获取特定公众号信息 - get_gzh_info

![ws_api.get_gzh_info('南航青年志愿者')](https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/get_gzh_info.png)

- 使用
```
In [5]: import wechatsogou
  ...:
  ...: ws_api =wechatsogou.WechatSogouAPI()
  ...: ws_api.get_gzh_info('南航青年志愿者')
  ...:
Out[5]:
{'authentication': '南京航空航天大学',
'headimage': 'http://img01.sogoucdn.com/app/a/100520090/oIWsFt1tmWoG6vO6BcsS7St61bRE',
'introduction': '南航大志愿活动的领跑者,为你提供校内外的志愿资源和精彩消息.',
'post_perm': 0,
'profile_url': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1501140102&ver=1&signature=OpcTZp20TUdKHjSqWh7m73RWBIzwYwINpib2ZktBkLG8NyHamTvK2jtzl7mf-VdpE246zXAq18GNm*S*bq4klw==',
'qrcode': 'http://mp.weixin.qq.com/rr?src=3&timestamp=1501140102&ver=1&signature=-DnFampQflbiOadckRJaTaDRzGSNfisIfECELSo-lN-GeEOH8-XTtM*ASdavl0xuavw-bmAEQXOa1T39*EIsjzxz30LjyBNkjmgbT6bGnZM=',
'wechat_id': 'nanhangqinggong',
'wechat_name': '南航青年志愿者'}
```

- 返回数据结构
```python
{
    'profile_url': '',  # 最近10条群发页链接
    'headimage': '',  # 头像
    'wechat_name': '',  # 名称
    'wechat_id': '',  # 微信id
    'post_perm': '',  # 最近一月群发数
    'qrcode': '',  # 二维码
    'introduction': '',  # 介绍
    'authentication': ''  # 认证
}
```

## 搜索公众号

![ws_api.search_gzh('南京航空航天大学')](https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/search_gzh.png)

- 使用
```
In [6]: import wechatsogou
   ...:
   ...: ws_api =wechatsogou.WechatSogouAPI()
   ...: ws_api.search_gzh('南京航空航天大学')
   ...:
Out[6]:
[{'authentication': '南京航空航天大学',
  'headimage': 'http://img01.sogoucdn.com/app/a/100520090/oIWsFt1MvjqspMDVvZjpmxyo36sU',
  'introduction': '南京航空航天大学官方微信',
  'post_perm': 0,
  'profile_url': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1501141990&ver=1&signature=S-7U131D3eQERC8yJGVAg2edySXn*qGVi5uE8QyQU034di*2mS6vGJVnQBRB0It9t9M-Qn7ynvjRKZNQrjBMEg==',
  'qrcode': 'http://mp.weixin.qq.com/rr?src=3&timestamp=1501141990&ver=1&signature=Tlp-r0AaBRxtx3TuuyjdxmjiR4aEJY-hjh0kmtV6byVu3QIQYiMlJttJgGu0hwtZMZCCntdfaP5jD4JXipTwoGecAze8ycEF5KYZqtLSsNE=',
  'wechat_id': 'NUAA_1952',
  'wechat_name': '南京航空航天大学'},
 {'authentication': '南京航空航天大学',
  'headimage': 'http://img01.sogoucdn.com/app/a/100520090/oIWsFtwVmjdK_57vIKeMceGXF5BQ',
  'introduction': '南京航空航天大学团委官方微信平台',
  'post_perm': 0,
  'profile_url': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1501141990&ver=1&signature=aXFQrSDOiZJHedlL7vtAkvFMckxBmubE9VGrVczTwS601bOIT5Nrr8Pcgs6bQ-oEd6jdQ0aK5WCQjNwMAhJnyQ==',
  'qrcode': 'http://mp.weixin.qq.com/rr?src=3&timestamp=1501141990&ver=1&signature=7Cpbd9CVQsXJkExRcU5VM6NuyoxDQQfVfF7*CGI-PTR0y6stHPtdSDqzAzvPMWz67Xz9IMF2TDfu4Cndj5bKxlsFh6wGhiLH0b9ZKqgCW5k=',
  'wechat_id': 'nuaa_tw',
  'wechat_name': '南京航空航天大学团委'},
 ...]
```

- 数据结构

list of dict, dict:

```python
{
    'profile_url': '',  # 最近10条群发页链接
    'headimage': '',  # 头像
    'wechat_name': '',  # 名称
    'wechat_id': '',  # 微信id
    'post_perm': '',  # 最近一月群发数
    'qrcode': '',  # 二维码
    'introduction': '',  # 介绍
    'authentication': ''  # 认证
}
```

## 搜索微信文章

![ws_api.search_article('南京航空航天大学')](https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/search_article.png)

- 使用
```
In [7]: import wechatsogou
   ...:
   ...: ws_api =wechatsogou.WechatSogouAPI()
   ...: ws_api.search_article('南京航空航天大学')
   ...:
Out[7]:
[{'article': {'abstract': '【院校省份】江苏【报名时间】4月5日截止【考试时间】6月10日-11日南京航空航天大学2017年自主招生简章南京航空航天大学2017...',
   'imgs': ['http://img01.sogoucdn.com/net/a/04/link?appid=100520033&url=http://mmbiz.qpic.cn/mmbiz_png/P07yicBRJfC71QB3lREx4J4x34QOibGaia5BkiaaiaiaibicWkTBULou9R08K6FaxlUA1RFBFWCmpO1Lepk7ZcXK45vguQ/0?wx_fmt=png'],
   'time': 1490270644,
   'title': '南京航空航天大学2017年自主招生简章',
   'url': 'http://mp.weixin.qq.com/s?src=3&timestamp=1501142580&ver=1&signature=hRMlQOLQpu4BNhBACavusZdmk**D65qHyz5LWDq1lPjVcm7*iiBS0l7Pq40h0fiCX*bZ8vSMLzAMDNzELYFKIQ7mND0-7cQi-N0BtfTBql*CQdsHun-GtaYEqRva6Ukwce3gZh46SXJzo90kyZ3dwVYl6*589bGDIzG6JTGfpxI='},
  'gzh': {'headimage': 'http://wx.qlogo.cn/mmhead/Q3auHgzwzM5kiawibor6ABhnibMYnOADvqdcrl5XWiaFfM5mGYZ8cUica6A/0',
   'isv': 0,
   'profile_url': 'http://mp.weixin.qq.com/profile?src=3&timestamp=1501142580&ver=1&signature=dVkDdcFr1suL1WHdCOJj7pwZhG9W*APi-j5kRtS09ccv-WID-zNs0ecDiiz1wwE7qbNSk5HBL*ffpyVXcF0fFQ==',
   'wechat_name': '自主招生在线'}},
 ...]
```

- 数据结构

list of dict, dict:
```python
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
```

## 解析最近文章页 - get_gzh_artilce_by_history

![ws_api.search_article('南京航空航天大学')](https://raw.githubusercontent.com/chyroc/wechatsogou/master/screenshot/search_article.png)


- 使用
```
In [1]: import wechatsogou
   ...:
   ...: ws_api =wechatsogou.WechatSogouAPI()
   ...: ws_api.get_gzh_artilce_by_history('南航青年志愿者')
   ...:
Out[1]:
{'article': [{'abstract': '我们所做的，并不能立马去改变什么——\n但千里之行，绿勤行永不止步。\n我们不会就此止步，之后我们又将再出发。\n 民勤，再见。\n绿勤行，不再见。',
   'author': '',
   'content_url': 'http://mp.weixin.qq.com/s?timestamp=1501143158&src=3&ver=1&signature=B-*tqUrFyO7OqpFeJZwTA7JJtsHpz6BgC8ugyfgpOnyWLtPb85R5Zmu0JuZRbZKG72x4bQjMCcsfA5mC3GSSOPbYd-9tzvTgmroGRmc4Tzk8090KCiEu6EjA0YMHeytWJWpxr51M2FUYQhTWJ01pTmNnXLVAG6Ex6AG52uvvmQA=',
   'copyright_stat': 100,
   'cover': 'http://mmbiz.qpic.cn/mmbiz_jpg/icFYWMxnmxHDYgXNjAle7szYLgQmicbaQlb1eVFuwp2vxEu5eNVwYacaHah2N5W8dKAm725vxv5aM6DFlM59Wftg/0?wx_fmt=jpeg',
   'datetime': 1501072594,
   'fileid': 502326199,
   'main': 1,
   'send_id': 1000000306,
   'source_url': '',
   'title': '绿勤行——不说再见',
   'type': '49'},
   ...]
```
- 数据结构
```python
{
    'gzh_info': {
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

```

---

# TODO
- [x] 相似文章的公众号获取
- [x] 主页热门公众号获取
- [x] 文章详情页信息
- [x] 所有类型的解析
- [x] 验证码识别
- [ ] 接入爬虫框架
- [x] 兼容py2

---
