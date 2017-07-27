# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import io
import os
import unittest
import datetime

from nose.tools import assert_equal, assert_in, assert_true, assert_greater_equal

from wechatsogou.structuring import WechatSogouStructuring
from test import fake_data_path

assert_equal.__self__.maxDiff = None


class TestStructuringGzh(unittest.TestCase):
    def test_get_gzh_by_search(self):
        file_name = '{}/{}/{}'.format(os.getcwd(), fake_data_path, 'search-gaokao-gzh.html')
        with io.open(file_name, encoding='utf-8') as f:
            search_gaokao_gzh = f.read()

        gzh_list = WechatSogouStructuring.get_gzh_by_search(search_gaokao_gzh)

        names = []
        wechat_ids = []
        post_perms = []
        introductions = []
        authentications = []
        assert_equal(10, len(gzh_list))
        for gzh in gzh_list:
            names.append(gzh['wechat_name'])
            wechat_ids.append(gzh['wechat_id'])
            post_perms.append(gzh['post_perm'])
            introductions.append(gzh['introduction'])
            authentications.append(gzh['authentication'])

            assert_in('mp.weixin.qq.com/profile?src=3&timestamp=', gzh['profile_url'])
            assert_in('mp.weixin.qq.com/rr?src=', gzh['qrcode'])
            assert_in('img01.sogoucdn.com/', gzh['headimage'])

        assert_equal(['山东高考指南',
                      '高考家长圈',
                      '河南高考指南',
                      '高考360',
                      '云天高考',
                      '腾讯高考',
                      '高考快讯',
                      '专业中高考教育',
                      '晟嘉高考',
                      '新东方在线高考辅导'],
                     names)
        assert_equal([u'sdgkzn',
                      u'sinagkjzq',
                      u'hngaokao',
                      u'sctvgaokao360',
                      u'yuntiangaokao',
                      u'qq_gaokao',
                      u'gkkx678',
                      u'gh_591a43050b5f',
                      u'tjsjgk',
                      u'koogaokao'],
                     wechat_ids)
        assert_equal([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], post_perms)
        assert_equal(
            ['这里是山东最权威最专业的高考交流平台,由山东商报徐玉芹教育工作室独家运作.本平台与山东商报高考交流群互为依托,为山东考生和家长提供最及时、最准确的高考政策及信息解读,以及一流的填报志愿咨询服务.合作...',
             '定期推送高三家长关注的优秀家长经验交流、志愿填报技巧、考生心理辅导方法、考前营养搭配等诸多优质内容;为家长搭建交流互动平台.',
             '发布最新高考政策,分享高效学习方法,制定高考应试策略.考点总结政策分析名校介绍高考大纲试卷解析艺考文化课,权威专业的高考资讯一手掌握.',
             '360天,360度,用心伴您升学路.四川电视台科教频道每晚7:45播出.',
             '高端教育品牌,高分考生的加油站,重点中学的合作伙伴.开阔考生视野、提升认知,在以“研究”为主线的基础上,将考生培养成一个全面型的人才.课程特色,全科协调、单科精讲.云天高考一直深受高分考生和家长的追...',
             '腾讯高考频道是中国最具互动性高考门户网站.主要为中国高考生及家长提供有价值的资讯和辅导.内容包括:新闻、评论、视频、各科辅导、志愿填报、家长指南等多方面.',
             '高考快讯平台专为考生家长提供最新高考资讯、志愿填报指南、名校排行榜、状元经验、学习方法、高分秘籍等等,我们的努力将伴随着您圆大学梦,欢迎关注阅读!',
             '旨在做最专业的中高考教育交流平台,第一时间传递权威的中高考资讯,为孩子的未来保驾护航!',
             '关于天津高考,你关注我们一个就够啦!',
             '提供高考资讯、高考院校库、在线答疑、政策解读及试题发布.'],
            introductions)
        assert_equal(['《山东商报》社',
                      '新浪网技术(中国)有限公司',
                      '郑州新东方培训学校',
                      '四川省电化教育馆(四川教育电视台)',
                      '北京云天共业教育科技有限公司',
                      '深圳市腾讯计算机系统有限公司',
                      '广州卓越教育培训中心',
                      '大连沙河口科苑文化培训学校',
                      '天津市南开区晟嘉培训中心',
                      '北京新东方迅程网络科技股份有限公司'],
                     authentications)

    def test_get_article_by_search(self):
        file_name = '{}/{}/{}'.format(os.getcwd(), fake_data_path, 'search-gaokao-article.html')
        with io.open(file_name, encoding='utf-8') as f:
            search_gaokao_article = f.read()

        article_list = WechatSogouStructuring.get_article_by_search(search_gaokao_article)

        titles = []
        abstracts = []
        gzh_names = []
        isvs = []
        assert_equal(10, len(article_list))
        for i in article_list:
            article = i['article']
            titles.append(article['title'])
            abstracts.append(article['abstract'])

            assert_in('mp.weixin.qq.com/s?src=3&timestamp=', article['url'])
            assert_true(isinstance(article['imgs'], list))
            assert_greater_equal(len(article['imgs']), 1)

            gzh = i['gzh']

            assert_in('mp.weixin.qq.com/profile?src=3&timestamp', gzh['profile_url'])
            assert_in('wx.qlogo.cn/mmhead', gzh['headimage'])
            gzh_names.append(gzh['wechat_name'])
            isvs.append(gzh['isv'])

        # article
        assert_equal(['高考有多重要,为什么要重视高考?丨微观点',
                      '高考:穷人考不好,中产考状元,精英不高考',
                      '关于高考志愿的一点建议,仅供参考!',
                      '刚刚,高考“满分”诞生了!(附各省高考分数线)',
                      '高考学霸榜出炉!义乌最高分是她!排名...',
                      '【高考】权威发布!2017年我省高考各项日程',
                      '【高考】黑龙江省2017年普通高考成绩即将发布',
                      '高考2017 | 全国各省区市高考录取时间大汇总,最新最全!',
                      '高考志愿这么填,等于多考20分!这位特级教师的志愿填报方法很管用!',
                      '高考填志愿,如何选专业?学长学姐有话说'],
                     titles)
        assert_equal(['针对这个问题,其实占豪已经谈过,但还是想借高考之后、借这位小战友的留言,结合自己的人生经验,谈谈个人对这件事的看法....',
                      '#条条大路通罗马,有人就出生在罗马#前几天北京文科高考状元熊轩昂接受澎湃新闻的采访的时候,说了下面这段话. “农村地区的...',
                      '最近一直有哥迷留言问,填报高考志愿该选什么专业? 讲真,这个问题很难回答.专业选择没有绝对的好坏对错,跟考试成绩、个人兴...',
                      '高考会有满分的情况吗?还真有!6月22日开始,全国各省的高考成绩陆续发布.22日晚上,成都市青白江区一个小区内人声鼎沸,因...',
                      '浙江新高考各类别各段分数线及考生成绩于昨日揭晓.考生可凭考生号、密码查询自己的考试成绩!今年的高考成绩,经浙江省教育考...',
                      '根据我省招生录取工作安排,现将近期有关高考工作日程公布如下:一、高考成绩公布时间6月24日左右省招考院通过黑龙江省招生考...',
                      '黑龙江省2017年普通高考成绩即将发布 我省今年高考网上评卷工作现已结束,经过成绩核查、成绩校验等多个环节后,我省高考成绩...',
                      '2017年高考录取工作开始了,各省区市高考录取工作何时进行?为了方便考生和家长及时了解,小编为大家作了最新最全的梳理.(图...',
                      '各地高考成绩已陆续公布,在本公众号回复“高考查分”即可查询!~长按二维码即可关注本车~自昨天开始,全国各省份陆续公布...',
                      '导语高考成绩和批次线已经出来了,想必同学们已经开始进入另一重要环节——志愿填报.你是不是在为选专业而纠结痛苦?不怕!...'],
                     abstracts)

        # gzh
        assert_equal(['占豪',
                      '才华有限青年',
                      '新闻哥',
                      '光明网',
                      '义乌十八腔',
                      '龙招港',
                      '龙招港',
                      '微言教育',
                      '高考直通车',
                      '阳光高考信息平台', ],
                     gzh_names)
        assert_in(1, isvs)
        assert_in(0, isvs)

    def test_get_gzh_info_by_history(self):
        file_name = '{}/{}/{}'.format(os.getcwd(), fake_data_path, 'bitsea-history.html')
        with io.open(file_name, encoding='utf-8') as f:
            gzh_history = f.read()

        gzh_info = WechatSogouStructuring.get_gzh_info_by_history(gzh_history)

        assert_equal('槽边往事', gzh_info['name'])
        assert_equal('bitsea', gzh_info['wechat_id'])
        assert_equal('和菜头的微信Blog，用于分享各种新鲜资讯', gzh_info['authentication'])
        assert_equal('http://wx.qlogo.cn/mmhead/Q3auHgzwzM6zmSwQkvHdgXDtnpAyLYjuib8QdW6ibKKGo8zcZVbYxiaUw/0',
                     gzh_info['headimage'])
        assert_equal(' ', gzh_info['introduction'])

    def test_get_article_by_history_json(self):
        file_name = '{}/{}/{}'.format(os.getcwd(), fake_data_path, 'bitsea-history.html')
        with io.open(file_name, encoding='utf-8') as f:
            gzh_history = f.read()

        article_list = WechatSogouStructuring.get_article_by_history_json(gzh_history)
        titles = []
        urls = []
        digests = []
        for i in article_list:
            assert_equal('和菜头', i['author'])
            assert_equal('49', i['type'])
            assert_in('mp.weixin.qq.com/s?timestamp=', i['content_url'])
            assert_in(i['copyright_stat'], [11, 100])
            assert_in('mmbiz.qpic.cn/mmbiz_jpg/', i['cover'])
            assert_greater_equal(datetime.datetime.fromtimestamp(i['datetime']), datetime.datetime(2000, 1, 1))

            urls.append(i['content_url'])
            titles.append(i['title'])
            digests.append(i['digest'])

        assert_equal(
            ['帝都深处好修行',
             '如果我有个好一点的初中英文老师',
             '【广告】让手机清凉一哈',
             '写给各位陛下',
             '可能是年度电影的《大护法》',
             '怎样决定要不要去相信一个人',
             '照亮世界的那个人',
             '《冈仁波齐》观后',
             '没有什么火候不火候的',
             '完美受害人', ],
            titles)

        assert_equal([
            'http://mp.weixin.qq.com/s?timestamp=1500903767&src=3&ver=1&signature=X4l0IQ091w0DY2ERU7fD*h0VUwBxeHPOJH-Uk-vAfaPamMl6ij7fqAIHomnXQ2X2*2J94H0pixVjsjEkL0TbILtKInZ4hqPp3-lC1nQZcN9Fd*BGbTQp7WlZyzLvCXy0Z8yFVF*lIDlo75pemv7kW8wov4Hz5-uiVzBT5q*Nwaw=',
            'http://mp.weixin.qq.com/s?timestamp=1500903767&src=3&ver=1&signature=X4l0IQ091w0DY2ERU7fD*h0VUwBxeHPOJH-Uk-vAfaPamMl6ij7fqAIHomnXQ2X2*2J94H0pixVjsjEkL0TbIPsfeXemAw1IR5Pt5J*6JqjpgotoKPL*6eVHbdcbi4JCEfsnhbnsQUTLQWpBZe5UILx8062e6A2L00LyjQArkxU=',
            'http://mp.weixin.qq.com/s?timestamp=1500903767&src=3&ver=1&signature=X4l0IQ091w0DY2ERU7fD*h0VUwBxeHPOJH-Uk-vAfaPamMl6ij7fqAIHomnXQ2X2*2J94H0pixVjsjEkL0TbIOVd*HwElAYiJum8Q6su3tILWksr-4u9WZPSrfT7A6nErJ3f0kW8V1Jv9evurTe5X4pQrjjCZcE6WeYGwDJIH0Q=',
            'http://mp.weixin.qq.com/s?timestamp=1500903767&src=3&ver=1&signature=X4l0IQ091w0DY2ERU7fD*h0VUwBxeHPOJH-Uk-vAfaPamMl6ij7fqAIHomnXQ2X2*2J94H0pixVjsjEkL0TbIBtaRJpx-JbQsm-5X*GWfaS-jBtKyhOmAxio5OIROqwV71OrvtaxYq1oZG-WM9apKbLGDPIBc0sCFUB4WBOagwk=',
            'http://mp.weixin.qq.com/s?timestamp=1500903767&src=3&ver=1&signature=X4l0IQ091w0DY2ERU7fD*h0VUwBxeHPOJH-Uk-vAfaPamMl6ij7fqAIHomnXQ2X2*2J94H0pixVjsjEkL0TbID-eM8BIKq1ef1ajiKO1jz1k0E6xa1ROpt2Eo3Af6OHQGfYIq-WrfEsn3jLwps1V*TXmP6443wUYgrrStzJwKPc=',
            'http://mp.weixin.qq.com/s?timestamp=1500903767&src=3&ver=1&signature=X4l0IQ091w0DY2ERU7fD*h0VUwBxeHPOJH-Uk-vAfaPamMl6ij7fqAIHomnXQ2X2*2J94H0pixVjsjEkL0TbIJenG0s3GyCaMQIK18U3CHsWrrGwuL5Z0X*DSoztV49L-ZPrf39mbml1GBkZnX*gueDdUJBIHgvyFsaVCTePLrI=',
            'http://mp.weixin.qq.com/s?timestamp=1500903767&src=3&ver=1&signature=X4l0IQ091w0DY2ERU7fD*h0VUwBxeHPOJH-Uk-vAfaPamMl6ij7fqAIHomnXQ2X2*2J94H0pixVjsjEkL0TbIE2LQ5dJqrG018DC4M7E5RQ3D4V1p*eBszVaqr2saxG864LssINc8RKcASbkdSDEMiguB9xwuMcJXgGANUpBjtg=',
            'http://mp.weixin.qq.com/s?timestamp=1500903767&src=3&ver=1&signature=X4l0IQ091w0DY2ERU7fD*h0VUwBxeHPOJH-Uk-vAfaPamMl6ij7fqAIHomnXQ2X2*2J94H0pixVjsjEkL0TbINN4P-L*qGaX0SopEwmBNGbOUc*Ad5D8TKEUZOPNduI4uupwRQFL*I4r151vpRYSA92EYzb34uf82WZJMa5-kTU=',
            'http://mp.weixin.qq.com/s?timestamp=1500903767&src=3&ver=1&signature=X4l0IQ091w0DY2ERU7fD*h0VUwBxeHPOJH-Uk-vAfaPamMl6ij7fqAIHomnXQ2X2*2J94H0pixVjsjEkL0TbIEhfSajMgMm4uzkdEhe*6MP8H9YKg1q38xqFlBV3*sJxgwupUV8b1Q2c6OhhBEZgCTyKQvHWnGLDLBH0gvC10zQ=',
            'http://mp.weixin.qq.com/s?timestamp=1500903767&src=3&ver=1&signature=X4l0IQ091w0DY2ERU7fD*h0VUwBxeHPOJH-Uk-vAfaPamMl6ij7fqAIHomnXQ2X2*2J94H0pixVjsjEkL0TbIBK5p9HtcN9dTEMbIU5Vspa3IaeGox55FYOfhNbWBL2Td4hxYt3GKGzRe-TlOPVlDWXuy8CvdD1ap1fmhNt9Cy0=']
            , urls)

        assert_equal(['善哉，善哉！',
                      '说出来今天的人根本不会信，我的初中英文老师李女士在上课的时候打毛衣。',
                      '奔走相告：过气网红接到新广告！请点击，请阅读，请留言！',
                      '陛下们！微臣有话要说！',
                      '对，我就那么说了，不服来咬我啊？',
                      '在一个现代商业社会里，如何决定要不要去相信一个人？如何把人际关系判定的时间精力节省下来？网络慈父和菜头是这么说的：',
                      '在一名凡夫身上，我看到了菩萨那样的行止。',
                      '昨晚看了电影《冈仁波齐》，我不喜欢。',
                      '如果你是厨艺初学者，忘掉火候，那不是你应该关心的事情。',
                      '野鸡给自己加戏，观众不说话，并不等于看不明白。', ], digests)

    def test_get_gzh_info_and_article_by_history(self):
        file_name = '{}/{}/{}'.format(os.getcwd(), fake_data_path, 'bitsea-history.html')
        with io.open(file_name, encoding='utf-8') as f:
            gzh_history = f.read()

        gzh_article_list = WechatSogouStructuring.get_gzh_info_and_article_by_history(gzh_history)
        assert_in('gzh_info', gzh_article_list)
        assert_in('article', gzh_article_list)


if __name__ == '__main__':
    unittest.main()
