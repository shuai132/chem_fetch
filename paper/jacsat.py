from typing import List

from lxml import etree

import utils
from data import News
from log import log
from paper_fetcher import PaperFetcher


class Jacsat(PaperFetcher):
    def fetch(self) -> List[News]:
        url_home = "https://pubs.acs.org"
        # http_prefix = url_home[0:url_home.find("//")]
        url_jacsat = url_home + "/journal/jacsat"
        news: List[News] = []
        html_text = utils.get_html_text(url_jacsat, self.debug, use_chrome=True)
        raw_html = etree.HTML(html_text)

        for raw_html_article in raw_html.xpath(
                '//div[@class="journal-home_section asap_articles"]//div[@class="grid-item slide-item" and not(@aria-role="listitem")]'):
            raw_html_article = etree.tostring(raw_html_article, encoding=str)
            html = etree.HTML(raw_html_article)

            item = News()
            item.type = "Article"
            item.datetime = html.xpath('//span[@class="pub-date-value"]/text()')[0]

            item.url = url_home + html.xpath('//div/div/h3/a/@href')[0]
            item.img = html.xpath('//div/div/div[1]/a/img/@src')[0]
            item.title = html.xpath('//div/div/h3/a/@title')[0]
            # item.desc = ""
            item.author_list = html.xpath('//ul[@title="list of authors"]/li/span/text()')

            item.from_ = "JACS"
            news.append(item)
        log.d("fetch part<1> news num now: %d" % len(news))
        for raw_html_article in raw_html.xpath(
                '//div[@class="col-xs-12 current_issue"]//div[@class="grid-item slide-item" and not(@aria-role="listitem")]'):
            raw_html_article = etree.tostring(raw_html_article, encoding=str)
            html = etree.HTML(raw_html_article)

            item = News()
            item.type = "Article"
            item.datetime = html.xpath('//div/div/div[3]/span[4]/text()')[0]

            item.url = url_home + html.xpath('//div/div/h3/a/@href')[0]
            item.img = html.xpath('//div/div/div[1]/a/img/@src')[0]
            item.title = html.xpath('//div/div/h3/a/@title')[0]
            # item.desc = ""
            item.author_list = html.xpath('//ul[@title="list of authors"]/text()')

            item.from_ = "JACS"
            news.append(item)
        log.d("fetch part<2> news num now: %d" % len(news))
        if self.debug:
            print("print all jacsat news:")
            for _item in news:
                print(utils.object_to_json(_item))
            print("len(news) =", len(news))

        return news
