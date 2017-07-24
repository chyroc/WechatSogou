# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, print_function

import io
import os
import unittest

from nose.tools import assert_equal, assert_in

from wechatsogou.refactor_structuring import WechatSogouStructuring

ws_structuring = WechatSogouStructuring()


class TestStructuringGzh(unittest.TestCase):
    def test_structuring_gzh(self):
        file_name = '{}/{}'.format(os.getcwd(), 'test/file/search-gaokao-gzh.html')
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
            names.append(gzh['name'])
            wechat_ids.append(gzh['wechat_id'])
            post_perms.append(gzh['post_perm'])
            introductions.append(gzh['introduction'])
            authentications.append(gzh['authentication'])

            assert_in('mp.weixin.qq.com/profile?src=3&timestamp=', gzh['url'])
            assert_in('mp.weixin.qq.com/rr?src=', gzh['qrcode'])
            assert_in('img01.sogoucdn.com/', gzh['img'])

        assert_equal(['山东高考指南', '高考家长圈', '河南高考指南', '高考360', '云天高考', '腾讯高考', '高考快讯', '专业中高考教育', '晟嘉高考', '新东方在线高考辅导'],
                     names)
        assert_equal(
            [u'sdgkzn', u'sinagkjzq', u'hngaokao', u'sctvgaokao360', u'yuntiangaokao', u'qq_gaokao', u'gkkx678',
             u'gh_591a43050b5f', u'tjsjgk', u'koogaokao'], wechat_ids)
        assert_equal([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], post_perms)
        assert_equal(
            ['这里是山东最权威最专业的高考交流平台,由山东商报徐玉芹教育工作室独家运作.本平台与山东商报高考交流群互为依托,为山东考生和家长提供最及时、最准确的高考政策及信息解读,以及一流的填报志愿咨询服务.合作...',
             '定期推送高三家长关注的优秀家长经验交流、志愿填报技巧、考生心理辅导方法、考前营养搭配等诸多优质内容;为家长搭建交流互动平台.',
             '发布最新高考政策,分享高效学习方法,制定高考应试策略.考点总结政策分析名校介绍高考大纲试卷解析艺考文化课,权威专业的高考资讯一手掌握.',
             '360天,360度,用心伴您升学路.四川电视台科教频道每晚7:45播出.',
             '高端教育品牌,高分考生的加油站,重点中学的合作伙伴.开阔考生视野、提升认知,在以“研究”为主线的基础上,将考生培养成一个全面型的人才.课程特色,全科协调、单科精讲.云天高考一直深受高分考生和家长的追...',
             '腾讯高考频道是中国最具互动性高考门户网站.主要为中国高考生及家长提供有价值的资讯和辅导.内容包括:新闻、评论、视频、各科辅导、志愿填报、家长指南等多方面.',
             '高考快讯平台专为考生家长提供最新高考资讯、志愿填报指南、名校排行榜、状元经验、学习方法、高分秘籍等等,我们的努力将伴随着您圆大学梦,欢迎关注阅读!',
             '旨在做最专业的中高考教育交流平台,第一时间传递权威的中高考资讯,为孩子的未来保驾护航!', '关于天津高考,你关注我们一个就够啦!', '提供高考资讯、高考院校库、在线答疑、政策解读及试题发布.'],
            introductions)
        assert_equal(['《山东商报》社', '新浪网技术(中国)有限公司', '郑州新东方培训学校', '四川省电化教育馆(四川教育电视台)', '北京云天共业教育科技有限公司', '深圳市腾讯计算机系统有限公司',
                      '广州卓越教育培训中心', '大连沙河口科苑文化培训学校', '天津市南开区晟嘉培训中心', '北京新东方迅程网络科技股份有限公司'], authentications)


if __name__ == '__main__':
    unittest.main()
