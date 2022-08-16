from typing import List


class News:
    def __init__(self):
        self.from_ = ""
        self.type = ""
        self.datetime = ""
        self.title = ""
        self.title_zh = ""
        self.url = ""
        self.img = ""
        self.desc = ""
        self.desc_zh = ""
        self.author_list: List[str] = []
