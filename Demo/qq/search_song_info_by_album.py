# -*- coding:utf-8 -*-
import urllib
import xlrd
import time
from urllib import request, parse
import json
from xlutils.copy import copy
import threading

response_json = {}


# 线程类
class MyThread(threading.Thread):
    def __init__(self, url, result__sheet):
        threading.Thread.__init__(self)
        self.url = url
        self.result__sheet = result__sheet

    # 读取源文件xls 获取需要搜索的字符串
    def run(self):
        try:
            result__sheet = self.result__sheet
            result__sheet.write(0, 0, '专辑名称')
            result__sheet.write(0, 1, '时间')
            result__sheet.write(0, 2, '歌手名称')
            result__sheet.write(0, 3, '流派')
            result__sheet.write(0, 4, '语种')
            result__sheet.write(0, 5, '发行公司')
            result__sheet.write(0, 6, '歌曲名称')
            j = 1
            response = str(getHtml(self.url))
            result_list = response[response.index('(') + 1: len(response) - 1]
            album_list = json.loads(result_list)['albumlib']['data']['list']
            for single_album in album_list:
                result__sheet.write(j, 0, single_album['album_name'])
                result__sheet.write(j, 1, single_album['public_time'])
                result__sheet.write(j, 2, single_album['singers'][0]['singer_name'])
                response = str(getHtml(album_mid=single_album['album_mid']))
                album_detail = json.loads(response[response.index('(') + 1: len(response) - 1])
                result__sheet.write(j, 3, album_detail['data']['genre'])
                result__sheet.write(j, 4, album_detail['data']['lan'])
                result__sheet.write(j, 5, album_detail['data']['company'])
                album_song_list = album_detail['data']['list']
                if album_song_list is not None:
                    for single_album_song in album_song_list:
                        result__sheet.write(j, 6, single_album_song['songname'])
                        j += 1
                else:
                    j += 1
                j += 1

        except TypeError as e:
            if hasattr(e, "code"):
                print(e.code)


# 整合请求头信息, 获取soup信息,解析结果
def getHtml(url=None, album_mid=""):
    global response_json
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/' \
                     '537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
        headers = {'User-Agent': user_agent}
        if url is None:
            url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_album_info_cp.fcg?albummid=" \
                  + album_mid + "&g_tk=5381&jsonpCallback=albuminfoCallback&loginUin=0&hostUin=0" \
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


# 启动线程
def startThread():
    source_xls = xlrd.open_workbook('E:/album.xls', formatting_info=True)
    result_xls = copy(source_xls)
    source_sheet = source_xls.sheet_by_index(0)
    for i in range(0, 5):
        if source_sheet.cell(i, 1).ctype == 0:
            continue
        url = source_sheet.cell(i, 1).value
        if source_sheet.cell(i, 0).ctype == 0:
            continue
        result__sheet = result_xls.add_sheet(source_sheet.cell(i, 0).value)
        thread = MyThread(url, result__sheet)
        thread.start()
        thread.join()
    result_xls.save('E:/album_result.xls')


begin_time = time.time()
startThread()
end_time = time.time()
print(end_time - begin_time)
