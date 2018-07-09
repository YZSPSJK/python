# -*- coding:utf-8 -*-
import urllib
import xlrd
import time
from urllib import request, parse
import json
from xlutils.copy import copy
import threading
import random

response_json = {}


# 线程类
class MyThread(threading.Thread):
    def __init__(self, thread_index, result__sheet, temp_list):
        threading.Thread.__init__(self)
        self.thread_index = thread_index
        self.result__sheet = result__sheet
        self.temp_list = temp_list

    # 读取源文件xls 获取需要搜索的字符串
    def run(self):
        try:
            result__sheet = self.result__sheet
            temp_list = self.temp_list
            thread_index = self.thread_index
            i = thread_index * 3075
            for search_word in temp_list:
                if isinstance(search_word, float) or isinstance(search_word, int):
                    search_word = int(search_word)
                response = str(getHtml(search_word))
                result_list = response[response.index('(') + 1: len(response) - 2]
                song_list = json.loads(result_list)['data']['lists']
                if len(song_list) > 0:
                    singer = ''
                    first_song = song_list[0]
                    result__sheet.write(i, 3, change_str(first_song['SongName']))
                    for single_singer in first_song['SingerName'].split('、'):
                        singer = singer + single_singer + '&'
                    if singer.find('&') != -1:
                        singer = singer[0:len(singer) - 1]
                    result__sheet.write(i, 4, change_str(singer))
                    result__sheet.write(i, 5, change_str(first_song['AlbumName']))
                else:
                    result__sheet.write(i, 3, 'none')
                i = i + 1
        except TypeError as e:
            print(e)  # 整合请求头信息, 获取soup信息,解析结果


def change_str(temp_str):
    if temp_str.find('<em>') != -1:
        return temp_str[4: len(temp_str) - 5]
    else:
        return temp_str


def getDogDictByWord(search_word):
    result_list = []
    for request_time in range(0, 3):
        response = str(getHtml(search_word))
        if response != '':
            break
        if request_time == 2:
            return '请求失败'
            i += 1
        continue
    json_list = response[response.index('(') + 1: len(response) - 2]
    song_list = json.loads(json_list)['data']['lists']
    if len(song_list) > 0:
        i = 0
        for each_song in song_list:
            i += 1
            if i > 20:
                break
            each_song_info = {}
            singer = ''
            for single_singer in each_song['SingerName'].split('、'):
                singer = singer + single_singer + '&'
            if singer.find('&'):
                singer = singer[0:len(singer) - 1]
            each_song_info['song'] = change_str(each_song['SongName'])
            each_song_info['singer'] = singer
            result_list.append(each_song_info)
    # time.sleep(random.uniform(0.2, 1.5))
    return result_list


def getHtml(search_word):
    global response_json
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/' \
                     '537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
        headers = {'User-Agent': user_agent}
        url = "http://songsearch.kugou.com/song_search_v2?callback=jQuery112403102033345133497_1530106881411&keyword=" \
              + parse.quote(str(search_word)) + \
              "&page=1&pagesize=30&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1530106881418"
        req_res = request.Request(url, headers=headers)
        response_result = request.urlopen(req_res).read()
        response_json = response_result.decode('utf-8')
    except TypeError as e:
        print(e)
    return response_json


# 启动线程
def startThread(source_file, result_file):
    source_xls = xlrd.open_workbook(source_file, formatting_info=True)
    result_xls = copy(source_xls)
    source_sheet = source_xls.sheet_by_index(0)
    result__sheet = result_xls.get_sheet(0)
    tsk = []
    for i in range(0, 16):
        temp_list = []
        for j in range(i * 3075, i * 3075 + 3075):
            if j >= 50000:
                break
            if source_sheet.cell(j, 0).ctype == 0:
                continue
            temp_list.append(source_sheet.cell(j, 0).value)
        temp_thread = MyThread(i, result__sheet, temp_list)
        temp_thread.start()
        tsk.append(temp_thread)
    for tt in tsk:
        tt.join()
    result_xls.save(result_file)


# begin_time = time.time()
# startThread('E:/hot_word.xls', 'E:/hot_word_dog.xls')
# end_time = time.time()
# print(end_time - begin_time)
