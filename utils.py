import json
import os

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import DIR_CACHE

CURRENT_DIR: str = os.path.split(os.path.realpath(__file__))[0]


def object_to_dict(obj):
    pr = {}
    for name in dir(obj):
        attr = getattr(obj, name)
        if name.startswith('__'):
            continue
        if callable(attr):
            continue
        if name.startswith('_'):
            name = name[1:]
        if name.endswith('_'):
            name = name[:-1]
        pr[name] = attr
    return pr


def object_to_json(obj):
    return json.dumps(object_to_dict(obj), indent=2)


def get_html_text(url: str, debug: bool, use_chrome=False):
    def request_url():
        if use_chrome:
            chrome_options = Options()
            # chrome_options.add_argument('headless')
            browser = webdriver.Chrome(chrome_options=chrome_options)
            browser.set_page_load_timeout(60)
            browser.get(url)
            return browser.page_source
        else:
            return requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36",
            }).text

    if debug:
        cache_html_file = DIR_CACHE + "/" + url.replace(':', '_').replace('/', '_') + ".html"
        try:
            with open(cache_html_file) as f:
                html_text = f.read()
        except FileNotFoundError:
            html_text = request_url()
            with open(cache_html_file, "w") as f:
                f.write(html_text)
    else:
        html_text = request_url()

    return html_text
