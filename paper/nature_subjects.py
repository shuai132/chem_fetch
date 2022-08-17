import re
from typing import List

from lxml import etree

import utils
from data import News
from paper_fetcher import PaperFetcher
from utils import get_html_text


class NatureSubjects(PaperFetcher):
    def fetch(self) -> List[News]:
        url_home = "https://www.nature.com"
        http_prefix = url_home[0:url_home.find("//")]
        url_ncomms = url_home + "/subjects/chemistry/ncomms"
        news: List[News] = []
        html_text = get_html_text(url_ncomms, self.debug)
        raw_html = etree.HTML(html_text)
        for raw_html_article in raw_html.xpath('//*[@id="content"]/div[2]/div/div/div/div[1]/ul/li/article'):
            raw_html_article = etree.tostring(raw_html_article, encoding=str)
            html = etree.HTML(raw_html_article)

            item = News()
            item.type = html.xpath('//div/p/span[1]/text()')[0]
            item.datetime = html.xpath('//div/p/time/text()')[0]

            raw_content = etree.tostring(html.xpath('//div/h3/a')[0], encoding=str)
            group = re.match(r"""<a href="(.*?)".*<img src="(.*?)".*/>(.*?)</a>""", raw_content, re.S)
            item.url = url_home + group[1]
            item.img = http_prefix + group[2]
            item.title = group[3].strip()

            try:
                raw_desc = etree.tostring(html.xpath('//div/div/p')[0], encoding=str)
                group = re.match(r"""<p>(.*?)</p>""", raw_desc, re.S)
                item.desc = group[1]
            except IndexError:
                pass

            try:
                index = 1
                while True:
                    author = html.xpath('//div/ul/li[%d]/span[2]/text()' % index)[0]
                    item.author_list.append(author)
                    index += 1
            except IndexError:
                pass

            item.from_ = "nat.c"
            news.append(item)

        if self.debug:
            print("print all nature news:")
            for item in news:
                print(utils.object_to_json(item))
            print("len(news) =", len(news))

        return news
