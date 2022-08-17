from typing import List

from lxml import etree

import utils
from data import News
from paper_fetcher import PaperFetcher
from utils import get_html_text


class Angew(PaperFetcher):
    def fetch(self) -> List[News]:
        url_home = "https://onlinelibrary.wiley.com"
        http_prefix = url_home[0:url_home.find("//")]
        url_articles = url_home + "/toc/15213773/0/0"
        news: List[News] = []
        html_text = get_html_text(url_articles, self.debug, True)
        raw_html = etree.HTML(html_text)

        div_title_should_skip = [
            'Cover Pictures',
            'Introducing …',
        ]

        count = 0
        div_title = ""
        div_title_from = "Article"
        next_issue_item_should_save = False
        for content_div in raw_html.xpath('//div[@class="table-of-content"]/div/*'):
            raw_html_content_div = etree.tostring(content_div, encoding=str)
            html = etree.HTML(raw_html_content_div)

            count = count + 1
            if content_div.tag == "h3":
                div_title = content_div.text
            if content_div.tag == "h4":
                div_title_from = content_div.text
            if div_title in div_title_should_skip:
                next_issue_item_should_save = False
                continue
            else:
                next_issue_item_should_save = True

            is_issue_item = content_div.attrib['class'] == "issue-item"
            if not is_issue_item:
                continue
            if not next_issue_item_should_save:
                continue

            item = News()
            item.type = div_title_from
            item.datetime = html.xpath('//li[@class="ePubDate"]/span/text()')[1]

            item.url = url_home + html.xpath('//a/@href')[0]
            item_img_url = html.xpath('//div[@class="toc-item__abstract abstract-preview"]/div/a/@href')
            if len(item_img_url) > 0:
                item.img = url_home + item_img_url[0]
            item.title = etree.tostring(html.xpath('//a/h2')[0], encoding=str).strip()[
                         len("<h2>"): -len("</h2>")].strip()

            # noinspection PyBroadException
            try:
                item.desc = etree.tostring(html.xpath('//div[@class="toc-item__abstract abstract-preview"]/div/p')[0],
                                           encoding=str).strip()[len("<p>"): -len("</p>")].strip()
            except Exception:
                pass

            item.author_list = html.xpath('//div[@class="comma__list"]/span/a/@title')

            item.from_ = "Angew"
            news.append(item)

        if self.debug:
            print("print all news:")
            for _item in news:
                print(utils.object_to_json(_item))
            print("len(news) =", len(news))

        return news
