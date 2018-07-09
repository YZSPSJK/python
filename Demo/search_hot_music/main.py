# -*- coding:utf-8 -*-
import urllib
import xlrd
import time
from urllib import request
import json
from xlutils.copy import copy


# 整合请求头信息, 获取soup信息,解析结果
def getHtml(url):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/' \
                     '537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
        headers = {'User-Agent': user_agent}
        req_res = request.Request(url, headers=headers)
        response_result = request.urlopen(req_res).read()
        response_json = response_result.decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return response_json


# 读取源文件xls 获取需要搜索的字符串
def readXlsFile():
    source_xls = xlrd.open_workbook('E:/hot_music.xls', formatting_info=True)
    result_xls = copy(source_xls)
    source_sheet = source_xls.sheet_by_index(0)
    for i in range(0, 11):
        j = 1
        if source_sheet.cell(i, 1).ctype == 0:
            continue
        url = source_sheet.cell(i, 1).value
        if source_sheet.cell(i, 0).ctype == 0:
            continue
        song_class = source_sheet.cell(i, 0).value
        result__sheet = result_xls.add_sheet(song_class)
        result__sheet.write(0, 0, '歌曲名称')
        result__sheet.write(0, 1, '歌手名称')
        result__sheet.write(0, 2, '专辑名称')
        response = str(getHtml(url))
        result_list = response[response.index('(') + 1: len(response) - 1]
        song_list = json.loads(result_list)['songlist']
        for single_song in song_list:
            song_detail = single_song['data']
            song_name = song_detail['songname']
            album_name = song_detail['albumname']
            singer_name = song_detail['singer'][0]['name']
            result__sheet.write(j, 0, song_name)
            result__sheet.write(j, 1, singer_name)
            result__sheet.write(j, 2, album_name)
            j += 1
    result_xls.save('E:/hot_music_result.xls')


begin_time = time.time()
readXlsFile()
end_time = time.time()
print(end_time - begin_time)
