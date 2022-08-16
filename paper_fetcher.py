import re
from typing import List

from data import News
from log import log


class PaperFetcher:
    def __init__(self, debug: bool = False):
        self.debug = debug

    def fetch(self) -> List[News]:
        pass

    def fetch_filter(self) -> List[News]:
        news = self.fetch()
        news = paper_filter(news)
        return news


def paper_filter(news: List[News]) -> List[News]:
    any_should_skip = [  # must lower case
        'protein', 'proteins', 'dna', 'rna',
        'chirality',
        'peptide',
        'biosynthesis',
        'perovskite',
        'supramolecular',
    ]

    any_should_skip_words = [  # must lower case
        'asymmetric synthesis',
        'drug delivery',
    ]

    def check_skip(s: str):
        s = s.lower()
        if "organic chemistry" in s and "inorganic chemistry" not in s:
            return True
        for words in any_should_skip_words:
            if words in s:
                return True
        for i in re.split(r'[^a-z]', s):
            if i.lower() in any_should_skip:
                return True
        return False

    count_before = len(news)
    ret_news: List[News] = []
    for item in news:
        if check_skip(item.title):
            log.d("skip title:", item.title)
            continue
        if check_skip(item.desc):
            log.d("skip desc:", item.desc)
            continue
        ret_news.append(item)
    count_after = len(ret_news)
    log.i("filter count: ", count_before - count_after)
    return ret_news
