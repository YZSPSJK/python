# -*- coding:utf-8 -*-
import urllib
import xlrd
import time
from urllib import request, parse
from bs4 import BeautifulSoup
from xlutils.copy import copy


# 整合请求头信息, 获取soup信息,解析结果
def getHtml(keyword):
    try:
        url = 'http://music.migu.cn/v2/search?keyword=' + parse.quote(keyword)
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
        soup = getHtml(source_str)
        song_list = soup.find_all('div', class_=['songlist-item', 'single-item'])
        temp_str = 'empty'
        for single_song in song_list:
            if len(single_song.attrs) == 1:
                continue
            song_detail = single_song.find_all('span', class_=['song-name-text'])
            if song_detail[0].a.attrs['title'].startswith(result_str) or song_detail[0].a.attrs[
                 'title'].upper().startswith(result_str.upper()):
                temp_str = single_song.find_all('div', class_=['song-number'])[0].string
                break
        result__sheet.write(i, 5, temp_str)
    result_xls.save('E:/result.xls')

begin_time = time.time()
readXlsFile()
end_time = time.time()
print(end_time-begin_time)

