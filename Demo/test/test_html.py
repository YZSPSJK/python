# -*- coding:utf-8 -*-
import urllib
import xlrd
import time
from urllib import request, parse
import json
from xlutils.copy import copy
import threading
import execjs

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
            i = thread_index * 250
            for search_word in temp_list:
                if i == 0:
                    i = i + 1
                    continue
                if isinstance(search_word, float) or isinstance(search_word, int):
                    search_word = int(search_word)
                response = str(getHtml(search_word))
                result_list = response[response.index('(') + 1: len(response) - 1]
                song_list = json.loads(result_list)['data']['song']['list']
                if len(song_list) > 0:
                    singer = ''
                    first_song = song_list[0]
                    result__sheet.write(i, 10, first_song['name'])
                    for single_singer in first_song['singer']:
                        singer = singer + single_singer['name'] + '&'
                    if singer.find('&'):
                        singer = singer[0:len(singer) - 1]
                    result__sheet.write(i, 11, singer)
                    result__sheet.write(i, 12, first_song['album']['name'])
                    # print(search_word)
                    i = i + 1
                    # print(first_song['name'])
                else:
                    result__sheet.write(i, 10, 'none')
                    i = i + 1
        except TypeError as e:
            print(e)  # 整合请求头信息, 获取soup信息,解析结果


def getHtml(search_word):
    global response_json
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/' \
                     '537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
        headers = {
            'User-Agent': user_agent, 'Referer': 'https://music.163.com/search/', 'Host': 'music.163.com',
            'Accept': '*/*', 'Accept-Language': 'en,zh-CN;q=0.9,zh;q=0.8',
            'Connection': 'keep-alive'}
        url = 'http://localhost:3000/search?keywords='+parse.quote(str(search_word))+'&type=1'
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
    result__sheet.write(0, 10, '歌曲名称')
    result__sheet.write(0, 11, '歌手名称')
    result__sheet.write(0, 12, '专辑名称')

    tsk = []
    for i in range(0, 16):
        temp_list = []
        for j in range(i * 250, i * 250 + 250):
            if j > 3943:
                break
            if source_sheet.cell(j, 1).ctype == 0:
                continue
            temp_list.append(source_sheet.cell(j, 1).value)
        temp_thread = MyThread(i, result__sheet, temp_list)
        temp_thread.start()
        tsk.append(temp_thread)
    for tt in tsk:
        tt.join()
    result_xls.save(result_file)


begin_time = time.time()
getHtml('你好')
end_time = time.time()
print(end_time - begin_time)
