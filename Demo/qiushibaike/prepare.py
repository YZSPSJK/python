# -*- coding:utf-8 -*-
import re
import urllib
from urllib import request
from bs4 import BeautifulSoup

for i in range(10):
    url = 'http://www.qiushibaike.com/hot/page/' + str(i)
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/' \
                     '537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
        headers = {'User-Agent': user_agent}

        req_res = request.Request(url, headers=headers)
        response_result = request.urlopen(req_res).read()
        content = response_result.decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)

    soup = BeautifulSoup(content, 'html.parser')

    items = soup.select('div .content')
    for item in items:
        if item.span.string is not None:
            print(item.span.string)
