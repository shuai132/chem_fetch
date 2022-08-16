import html
import re
import urllib.parse
import urllib.request


def unescape(text):
    parser = html
    return parser.unescape(text)


def translate(to_translate, to_language="zh-CN", from_language="auto"):
    base_link = "http://translate.google.com/m?tl=%s&sl=%s&q=%s"
    to_translate = urllib.parse.quote(to_translate)

    link = base_link % (to_language, from_language, to_translate)
    request = urllib.request.Request(link, headers={
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    })
    raw_data = urllib.request.urlopen(request).read()
    data = raw_data.decode("utf-8")

    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    re_result = re.findall(expr, data)
    if len(re_result) == 0:
        result = ""
    else:
        result = unescape(re_result[0])
    return result


if __name__ == '__main__':
    text_data = "The reduction of [TiCp*Cl] with magnesium leads to a mixed-valence titanium species capable of reacting with dinitrogen to form a stable trinuclear complex with a η : η : η-N ligand. This dinitrogen complex further reacts cleanly with HCl to produce NHCl with regeneration of the titanium precursor. Thus, a cyclic ammonia synthesis under ambient conditions can be envisaged."
    print(translate(text_data))
