import argparse
import os
import time
from typing import List

import config
import service
import utils
from config import DIR_CACHE
from data import News, AddNews
from log import log
from paper.angew import Angew
from paper.jacsat import Jacsat
from paper.nature_nchem import NatureNChem
from paper.nature_subjects import NatureSubjects
from translator import GoogleTranslator


def update_time():
    # todo: update_time misc
    # {"data": time.strftime('%Y-%m-%d %H:%M:%S')}
    pass


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--debug', type=bool, const=True, nargs='?')
    parser.add_argument('--log', type=bool, const=True, nargs='?')
    parser.add_argument('--force_update', type=bool, const=True, nargs='?')
    parser.add_argument('--loop', type=int, help='interval in minute')
    parser.add_argument('--admin_token', type=str)
    args = parser.parse_args()

    config.ADMIN_TOKEN = args.admin_token

    os.makedirs(DIR_CACHE, 0o755, True)
    log.debug = args.debug or args.log

    count_insert = 0
    count_update = 0

    service.init()

    def translate_news(item: News):
        log.i("translate_news...")
        if item.title.strip() != "" and item.title_zh == "":
            item.title_zh = GoogleTranslator.translate(item.title)
        if item.desc.strip() != "" and item.desc_zh == "":
            item.desc_zh = GoogleTranslator.translate(item.desc)
        log.d("title: en:", item.title)
        log.d("title: zh:", item.title_zh)
        log.d("desc: en:", item.desc)
        log.d("desc: zh:", item.desc_zh)

    def upload_news(news: List[News]):
        if args.force_update:
            for item in news:
                translate_news(item)
                nonlocal count_update
                count_update += 1
            return
        news.reverse()
        for item in news:
            translate_news(item)
            log.i("insert:", item.title)
            item.author_list = item.author_list.__str__()
            add_news = AddNews()
            add_news.news___ = item
            add_news.token = config.ADMIN_TOKEN
            rsp = service.request("add_news", utils.object_to_dict(add_news))
            log.i("result:", rsp.text)
            nonlocal count_insert
            count_insert += 1

    def fetch_and_update():
        papers = [
            NatureSubjects(args.debug),
            Jacsat(args.debug),
            NatureNChem(args.debug),
            Angew(args.debug),
        ]
        for paper in papers:
            try:
                log.i("fetch paper:", paper)
                paper_news = paper.fetch_filter()
                log.i("fetch num:", len(paper_news))
                if not args.debug:
                    upload_news(paper_news)
            except Exception as e:
                log.e("paper exception:", type(paper), e)
                if args.debug:
                    raise e

        if args.force_update:
            log.i("count_update:", count_update)
        log.i("count_insert:", count_insert)

        if not args.debug:
            update_time()

    fetch_and_update()
    loop_interval = args.loop
    if loop_interval:
        while True:
            log.i("%s, sleep for %d minute..." % (time.strftime('%Y-%m-%d %H:%M:%S'), loop_interval))
            time.sleep(60 * loop_interval)
            fetch_and_update()


if __name__ == '__main__':
    main()
