import os

DIR_CURRENT: str = os.path.split(os.path.realpath(__file__))[0]
DIR_CACHE = DIR_CURRENT + "/.cache"
FILE_RECORD = DIR_CACHE + "/record.json"

ADMIN_TOKEN = ""
