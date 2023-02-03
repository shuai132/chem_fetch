import requests

from log import log

HOST_URL = ""


def init():
    response = requests.get('https://gitee.com/shuai132/chem_server_url/raw/master/url.txt', timeout=3)
    global HOST_URL
    HOST_URL = response.text.strip()
    log.i("HOST_URL: ", HOST_URL)


def request(api, json_data):
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
