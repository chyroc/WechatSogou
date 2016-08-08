from wechatsogou import WechatSpider


def main():
    wechats = WechatSpider()
    infos = wechats.get_gzh_info('xichangyinhe3')
    # infos = wechats.get_gzh_info('newsbro')
    articledict = wechats.get_gzh_article_dict(infos['url'])
    articles = wechats.get_gzh_article_detail(articledict['msgdict'])
    for article in articles:
        article_info = wechats.get_gzh_article_info(article)
        print(article_info['content']['content_text'])

    # print(item)
    # print(item)
    # print(url)
    # print(article_list_infos)
    # print(infos)

if __name__ == "__main__":
    main()