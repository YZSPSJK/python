# -*- coding:utf-8 -*-
import urllib
import time
from urllib import request, parse
from bs4 import BeautifulSoup
import json
import threading
import xlwt


# 线程类
class MyThread(threading.Thread):
    def __init__(self, music_id, result__sheet):
        threading.Thread.__init__(self)
        self.music_id = music_id
        self.result__sheet = result__sheet

    # 读取源文件xls 获取需要搜索的字符串
    def run(self):
        try:
            result__sheet = self.result__sheet
            result__sheet.write(0, 0, '歌曲名称')
            result__sheet.write(0, 1, '歌手名称')
            soup = getHtml(self.music_id)
            song_list = soup.find_all(id="song-list-pre-cache")[0].find("textarea").get_text()
            song_json = json.loads(song_list)
            j = 1
            for single_song in song_json:
                result__sheet.write(j, 0, single_song['album']["name"])
                result__sheet.write(j, 1, single_song['artists'][0]["name"])
                j = j + 1
        except TypeError as e:
            if hasattr(e, "code"):
                print(e.code)


# 整合请求头信息, 获取soup信息,解析结果
def getHtml(music_id):
    try:
        url = 'http://music.163.com/discover/toplist?id=' + str(music_id)
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


# 启动线程
def startThread():
    result_workbook = xlwt.Workbook()
    music_id_list = [19723756, 3779629, 2884035, 3778678, 1978921795, 991319590,71385702,10520166,3812895,60131,71384707,180106,60198,11641012,27135204]
    for music_id in music_id_list:
        result__sheet = result_workbook.add_sheet(str(music_id))
        thread = MyThread(music_id, result__sheet)
        thread.start()
        thread.join()
        result_workbook.save('E:/cloud_music_result.xls')


begin_time = time.time()
startThread()
end_time = time.time()
print(end_time - begin_time)
