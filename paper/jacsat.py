from typing import List

from lxml import etree

import utils
from data import News
from log import log
from paper_fetcher import PaperFetcher


class Jacsat(PaperFetcher):
    def fetch(self) -> List[News]:
        url_home = "https://pubs.acs.org"
        url_jacsat = url_home + "/toc/jacsat/current"
        news: List[News] = []
        html_text = utils.get_html_text(url_jacsat, self.debug, use_chrome=True)
        raw_html = etree.HTML(html_text)

        def try_parser_news(raw_html_article: str):
            try:
                raw_html_article = etree.tostring(raw_html_article, encoding=str)
                html = etree.HTML(raw_html_article)

                if len(html.xpath('//div[@class="issue-item clearfix"]')) == 0:
                    log.d("skip not issue-item clearfix...")
                    return

                item = News()
                item.type = "Article"

                item.url = url_home + html.xpath('//div[3]/span/h5/a/@href')[0]

                item_img = html.xpath('//div[2]/img/@src')
                if len(item_img) == 0:
                    item_img = html.xpath('//div[2]/img/@data-src')
                item.img = url_home + item_img[0]

                item.title = html.xpath('//div[3]/span/h5/a/@title')[0]

                for author in html.xpath('//div[3]/ul/li'):
                    word_list = author.xpath("span/*/text()")
                    item.author_list.append(" ".join(word_list).replace(" *", "*"))

                item.datetime = html.xpath('//span[@class="pub-date-value"]/text()')[0]

                # item.desc = ""

                item.from_ = "JACS"
                news.append(item)
                log.d("add news: ", item.title)
            except LookupError as e:
                log.e("LookupError:", e)

        for article in raw_html.xpath(
                '//*[@id="pb-page-content"]/div/main/div[3]/div/div')[1:]:
            try_parser_news(article)

        log.d("fetch news num: %d" % len(news))
        if self.debug:
            print("print all jacsat news:")
            for _item in news:
                print(utils.object_to_json(_item))
            print("len(news) =", len(news))

        return news
