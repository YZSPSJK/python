# -*- coding:utf-8 -*-
import urllib
import xlrd
import time
from urllib import request, parse
import json

import xlwt
from xlutils.copy import copy
import threading

response_json = {}


# 线程类
class MyWorkBookThread(threading.Thread):
    def __init__(self, file_index, result_workbook):
        threading.Thread.__init__(self)
        self.result_workbook = result_workbook
        self.file_index = file_index

    # 读取源文件xls 获取需要搜索的字符串
    def run(self):
        name = 'E:/song_list_qq' + str(self.file_index) + '.xls'
        for i in range(0, 10):
            result__sheet = self.result_workbook.add_sheet(str(i + 1))
            thread = MyThread(self.file_index, i, result__sheet)
            thread.start()
            thread.join()
        self.result_workbook.save(name)


# 线程类
class MyThread(threading.Thread):
    def __init__(self, page, music_index, result__sheet):
        threading.Thread.__init__(self)
        self.result__sheet = result__sheet
        self.page = page
        self.music_index = music_index

    # 读取源文件xls 获取需要搜索的字符串
    def run(self):
        try:
            result__sheet = self.result__sheet
            result__sheet.write(0, 0, '歌单名称')
            result__sheet.write(0, 1, '歌单作家')
            result__sheet.write(0, 2, '播放量')
            result__sheet.write(0, 3, '标签')
            result__sheet.write(0, 4, '歌曲')
            result__sheet.write(0, 5, '歌手')
            result__sheet.write(0, 6, '专辑')
            song_list_referer = 'https://y.qq.com/portal/playlist.html'
            j = 1
            start_page_num = self.page * 600 + self.music_index * 60
            song_list_url = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?picmid=1&rnd=0.251761445296639' \
                            '&g_tk=5381&jsonpCallback=getPlaylist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8' \
                            '&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&categoryId=10000000&sortId=5&sin=' + str(
                start_page_num) + '&ein=' + str(start_page_num + 59)
            response = str(getHtml(song_list_url, song_list_referer))
            result_list = response[response.index('(') + 1: len(response) - 1]
            album_list = json.loads(result_list)['data']['list']
            for single_album in album_list:
                result__sheet.write(j, 0, single_album['dissname'])
                result__sheet.write(j, 1,
                                    single_album['creator']['name'] + '(' + str(
                                        single_album['creator']['qq']) + ')')
                result__sheet.write(j, 2, single_album['listennum'])
                song_url = 'https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1' \
                           '&utf8=1&onlysong=0&disstid=' + single_album['dissid'] + '&format=jsonp&g_tk=5381' \
                                                                                    '&jsonpCallback=playlistinfoCallback&loginUin=0&hostUin=0' \
                                                                                    '&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
                song_referer = 'https://y.qq.com/n/yqq/playsquare/' + single_album['dissid'] + '.html'
                song_response = str(getHtml(song_url, song_referer))
                song_result_list = song_response[song_response.index('(') + 1: len(song_response) - 1]
                all_song_list = json.loads(song_result_list)['cdlist'][0]['songlist']
                tags = json.loads(song_result_list)['cdlist'][0]['tags']
                all_tag = ''
                for tag in tags:
                    all_tag = all_tag + tag['name']
                result__sheet.write(j, 3, all_tag)
                for single_song in all_song_list:
                    result__sheet.write(j, 4, single_song['songname'])
                    if len(single_song['singer']) > 0:
                        result__sheet.write(j, 5, single_song['singer'][0]['name'])
                    else:
                        result__sheet.write(j, 5, '')
                    result__sheet.write(j, 6, single_song['albumname'])
                    j = j + 1
                j = j + 2
        except TypeError as e:
            if hasattr(e, "code"):
                print(e.code)


# 整合请求头信息, 获取soup信息,解析结果
def getHtml(url=None, referer=None):
    global response_json
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/' \
                     '537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
        headers = {'User-Agent': user_agent, 'referer': referer}
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
    for i in range(0, 11):
        result_workbook = xlwt.Workbook()
        thread = MyWorkBookThread(i, result_workbook)
        thread.start()


begin_time = time.time()
startThread()
end_time = time.time()
print(end_time - begin_time)
