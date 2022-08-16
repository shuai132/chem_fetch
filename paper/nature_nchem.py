import re
from typing import List

from lxml import etree

import utils
from data import News
from log import log
from paper_fetcher import PaperFetcher
from utils import get_html_text


class NatureNChem(PaperFetcher):
    def fetch(self) -> List[News]:
        url_home = "https://www.nature.com"
        http_prefix = url_home[0:url_home.find("//")]
        url_articles = url_home + "/nchem/research-articles"
        news: List[News] = []
        html_text = get_html_text(url_articles, self.debug)
        raw_html = etree.HTML(html_text)
        for raw_html_article in raw_html.xpath('//*[@id="new-article-list"]/div/ul/li/div/article'):
            raw_html_article = etree.tostring(raw_html_article, encoding=str)
            html = etree.HTML(raw_html_article)

            item = News()
            item.type = html.xpath('//div[2]/span/span/text()')[0]
            item.datetime = html.xpath('//div[2]/time/text()')[0]

            item.url = url_home + html.xpath('//div[1]/div[2]/h3/a/@href')[0]
            item.img = http_prefix + html.xpath('//div[1]/div[1]/picture/*/img/@src')[0]

            raw_content = etree.tostring(html.xpath('//div[1]/div[2]/h3/a')[0], encoding=str)
            group = re.match(r"""<a href=.*?>(.*?)</a>""", raw_content, re.S)
            item.title = group[1].strip()

            try:
                item.desc = html.xpath('//div[1]/div[2]/div/p/text()')[0]
            except:
                pass

            item.author_list = html.xpath('//div[1]/div[2]/ul/li/span/text()')

            item.from_ = "Nat.C"
            news.append(item)
        log.i("fetch Nat.C num: %d" % len(news))
        if self.debug:
            print("print all Nat.C news:")
            for _item in news:
                print(utils.object_to_json(_item))
            print("len(news) =", len(news))

        return news
