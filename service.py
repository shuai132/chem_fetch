import json

import requests

from log import log

HOST_URL = ""


def init():
    response = requests.get('https://gitee.com/shuai132/chem_server_url/raw/master/url.txt', timeout=3)
    global HOST_URL
    HOST_URL = response.text.strip()
    log.i("HOST_URL: ", HOST_URL)


def request(api: str, json_data: dict) -> requests.Response:
    headers = {
        'Connection': 'keep-alive'
    }

    response = requests.post(
        HOST_URL + '/api/' + api,
        headers=headers,
        json=json_data,
        timeout=3
    )

    log.d("request:", api, response.text)
    return response


def check_exist(url) -> bool:
    response = request("add_news", {
        "news": {
            "url": url,
        },
        "is_check": True,
    })
    rsp_json = json.loads(response.text)
    return rsp_json['data'] == 1


if __name__ == '__main__':
    init()
    log.i("check_exist:", check_exist("https://www.nature.com/articles/s41467-022-35371-6"))
