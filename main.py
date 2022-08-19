import argparse
import os
import time
from typing import List

import config
import utils
from bmob import Bmob
from config import FILE_RECORD, DIR_CACHE
from data import News
from log import log
from paper.angew import Angew
from paper.jacsat import Jacsat
from paper.nature_nchem import NatureNChem
from paper.nature_subjects import NatureSubjects
from recorder import Recorder
from translator import GoogleTranslator


def update_time():
    bmob = Bmob(config.BMOB_APP_ID, config.BMOB_APP_KEY)
    # noinspection PyBroadException
    try:
        item = bmob.find("misc", where={"id": "update_time"}).jsonData['results'][0]['objectId']
        bmob.update("misc", item, {"data": time.strftime('%Y-%m-%d %H:%M:%S')})
    except Exception:
        bmob.insert("misc", {"id": "update_time", "data": time.strftime('%Y-%m-%d %H:%M:%S')})


def main():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--debug', type=bool, const=True, nargs='?')
    parser.add_argument('--log', type=bool, const=True, nargs='?')
    parser.add_argument('--force_update', type=bool, const=True, nargs='?')
    parser.add_argument('--loop', type=int, help='interval in minute')
    parser.add_argument('--BMOB_APP_ID', type=str)
    parser.add_argument('--BMOB_APP_KEY', type=str)
    args = parser.parse_args()

    config.BMOB_APP_ID = args.BMOB_APP_ID
    config.BMOB_APP_KEY = args.BMOB_APP_KEY

    os.makedirs(DIR_CACHE, 0o755, True)
    log.debug = args.debug or args.log

    count_insert = 0
    count_update = 0

    recorder = Recorder(FILE_RECORD)

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
        bmob = Bmob(config.BMOB_APP_ID, config.BMOB_APP_KEY)
        if args.force_update:
            for item in news:
                translate_news(item)
                ret: List = bmob.find("news", where={"title": item.title}, keys={}, limit=1).jsonData["results"]
                if len(ret) == 0:
                    log.i("insert:", item.title)
                    bmob.insert("news", utils.object_to_dict(item))
                else:
                    log.i("update:", item.title)
                    bmob.update("news", ret[0]["objectId"], utils.object_to_dict(item))
                    nonlocal count_update
                    count_update += 1
            return
        news.reverse()
        for item in news:
            if recorder.check(item.title):
                log.i("ignore: cache:", item.title)
                continue

            try_times = 3
            ret = []
            while try_times:
                try_times -= 1

                # noinspection PyBroadException
                try:
                    ret: List = bmob.find("news", where={"title": item.title}, keys={}, limit=1).jsonData["results"]
                    time.sleep(1)
                    break
                except Exception:
                    if try_times == 0:
                        log.e("bmob.find error, will skip")
                        continue
                    else:
                        log.w("bmob.find error, will retry")

            if len(ret) == 0:
                translate_news(item)
                log.i("insert:", item.title)
                bmob.insert("news", utils.object_to_dict(item))
                nonlocal count_insert
                count_insert += 1
            else:
                log.i("ignore: blob:", item.title)
            recorder.record(item.title)

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

        recorder.save()

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
