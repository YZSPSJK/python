# -*- coding:utf-8 -*-
import urllib
import xlrd
import time
from urllib import request, parse
import json
from xlutils.copy import copy

response_json = {}


# 整合请求头信息, 获取soup信息,解析结果
def getHtml(url=None, album_mid=""):
    global response_json
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/' \
                     '537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
        headers = {'User-Agent': user_agent}

        if url is None:
            url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_album_info_cp.fcg?albummid=" + album_mid + "&g_tk=5381&jsonpCallback=albuminfoCallback&loginUin=0&hostUin=0" \
                                                                                                   "&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"
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
    try:
        source_xls = xlrd.open_workbook('E:/album.xls', formatting_info=True)
        result_xls = copy(source_xls)
        source_sheet = source_xls.sheet_by_index(0)
        for i in range(0, 5):
            j = 1
            if source_sheet.cell(i, 1).ctype == 0:
                continue
            url = source_sheet.cell(i, 1).value
            if source_sheet.cell(i, 0).ctype == 0:
                continue
            song_class = source_sheet.cell(i, 0).value
            result__sheet = result_xls.add_sheet(song_class)
            result__sheet.write(0, 0, '专辑名称')
            result__sheet.write(0, 1, '时间')
            result__sheet.write(0, 2, '歌手名称')
            result__sheet.write(0, 3, '流派')
            result__sheet.write(0, 4, '语种')
            result__sheet.write(0, 5, '发行公司')
            result__sheet.write(0, 6, '歌曲名称')
            response = str(getHtml(url))
            result_list = response[response.index('(') + 1: len(response) - 1]
            album_list = json.loads(result_list)['albumlib']['data']['list']
            for single_album in album_list:
                album_name = single_album['album_name']
                public_time = single_album['public_time']
                album_mid = single_album['album_mid']
                singer_name = single_album['singers'][0]['singer_name']
                result__sheet.write(j, 0, album_name)
                result__sheet.write(j, 1, public_time)
                result__sheet.write(j, 2, singer_name)
                response = str(getHtml(album_mid=album_mid))
                result_list = response[response.index('(') + 1: len(response) - 1]
                album_detail = json.loads(result_list)
                album_lan = album_detail['data']['lan']
                album_company = album_detail['data']['company']
                album_genre = album_detail['data']['genre']
                result__sheet.write(j, 3, album_genre)
                result__sheet.write(j, 4, album_lan)
                result__sheet.write(j, 5, album_company)
                album_song_list = album_detail['data']['list']
                if album_song_list is not None:
                    for single_album_song in album_song_list:
                        song_name = single_album_song['songname']
                        result__sheet.write(j, 6, song_name)
                        j += 1
                else:
                    j += 1
                j += 1
        result_xls.save('E:/album_result.xls')
    except TypeError as e:
        if hasattr(e, "code"):
            print(e.code)


begin_time = time.time()
readXlsFile()
end_time = time.time()
print(end_time - begin_time)
