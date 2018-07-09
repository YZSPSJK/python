# -*- coding:utf-8 -*-
import urllib
import xlrd
import time
from urllib import request, parse
from bs4 import BeautifulSoup
from xlutils.copy import copy


# 整合请求头信息, 获取soup信息,解析结果
def getHtml(keyword, page):
    try:
        url = 'http://music.migu.cn/v2/search?keyword=' + parse.quote(keyword)
        if page > 1:
            url = url + 'page=' + + parse.quote(page)
            print(url)
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
    return soup


# 读取源文件xls 获取需要搜索的字符串
def readXlsFile():
    source_xls = xlrd.open_workbook('E:/source.xls', formatting_info=True)
    result_xls = copy(source_xls)
    source_sheet = source_xls.sheet_by_index(0)
    result__sheet = result_xls.get_sheet(0)
    for i in range(2, 200):
        if source_sheet.cell(i, 3).ctype == 0:
            continue
        source_str = source_sheet.cell(i, 3).value
        result_str = source_sheet.cell(i, 4).value
        soup = getHtml(source_str, 1)
        song_list = soup.find_all('div', class_=['songlist-item', 'single-item'])
        temp_str = '00'
        for single_song in song_list:
            if len(single_song.attrs) == 1:
                continue
            song_detail = single_song.find_all('span', class_=['song-name-text'])
            if song_detail[0].a.attrs['title'].startswith(result_str) or song_detail[0].a.attrs[
                 'title'].upper().startswith(result_str.upper()):
                temp_str = single_song.find_all('div', class_=['song-number'])[0].string
                break

        # 获取当前搜索页的分页的页数,如果第一页没有匹配的 page-c iconfont cf-next-page
        if temp_str == 'empty':
            page = soup.find_all('div', class_=['page'])
            if page[0].content is not None:
                max_page = page[0].find_all('a', class_=['page-c', 'iconfont', 'cf-next-page'])[
                    0].find_previous_sibling().string
                temp_str = getNumber(max_page, result_str, source_str, temp_str)
        result__sheet.write(i, 5, temp_str)
    result_xls.save('E:/result.xls')


def getNumber(max_page, result_str, source_str, temp_str):
    for j in range(2, max_page):
        soup = getHtml(source_str, j)
        song_list = soup.find_all('div', class_=['songlist-item', 'single-item'])
        for single_song in song_list:
            if len(single_song.attrs) == 1:
                continue
            song_detail = single_song.find_all('span', class_=['song-name-text'])
            if song_detail[0].a.attrs['title'].startswith(result_str) or song_detail[0].a.attrs[
                 'title'].upper().startswith(result_str.upper()):
                temp_str = single_song.find_all('div', class_=['song-number'])[0].string
                return temp_str
    return temp_str

begin_time = time.time()
readXlsFile()
end_time = time.time()
print(end_time-begin_time)

