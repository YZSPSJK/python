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
    def __init__(self, music_param, result__sheet):
        threading.Thread.__init__(self)
        self.music_param = music_param
        self.result__sheet = result__sheet

    # 读取源文件xls 获取需要搜索的字符串
    def run(self):
        try:
            result__sheet = self.result__sheet
            result__sheet.write(0, 0, '歌曲名称')
            result__sheet.write(0, 1, '歌手名称')
            soup = getHtml(self.music_param)
            song_list = soup.find_all('div', class_='billboard-item songlist-item')
            j = 1
            for single_song in song_list:
                all_singer = single_song.find_all('a', class_="singer-text")
                singer_name = ''
                for singer in all_singer:
                    singer_name = singer_name+singer.text+','
                result__sheet.write(j, 0, single_song.find_all('span', class_="song-name-text")[0].text)
                result__sheet.write(j, 1, singer_name[0:len(singer_name)-1])
                j = j + 1
            page_soap = soup.find_all('div', class_='page')[0]
            page = len(page_soap.find_all('a'))
            for i in range(2, page):
                soup = getHtml(self.music_param, i)
                song_list = soup.find_all('div', class_='billboard-item songlist-item')
                for single_song in song_list:
                    all_singer = single_song.find_all('a', class_="singer-text")
                    singer_name = ''
                    for singer in all_singer:
                        singer_name = singer_name + singer.text + ','
                    result__sheet.write(j, 0, single_song.find_all('span', class_="song-name-text")[0].text)
                    result__sheet.write(j, 1, singer_name[0:len(singer_name)-1])
                    j = j + 1
        except TypeError as e:
            if hasattr(e, "code"):
                print(e.code)


# 整合请求头信息, 获取soup信息,解析结果
def getHtml(music_param=None, music_page=None):
    try:
        url = 'http://music.migu.cn/v2/music/billboard'
        if music_param is not None:
            url = url + '?' + music_param
        if music_param is not None and music_page is not None:
            url = url + '&page=' + str(music_page)
        if music_param is None and music_page is not None:
            url = url + '?page=' + str(music_page)
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
    first_soup = getHtml()
    billboard = first_soup.find_all('div', class_='sord-item on')
    first_sheet_name = billboard[0].find_all('span')[0].get_text()
    result__sheet = result_workbook.add_sheet(str(first_sheet_name))
    thread = MyThread(None, result__sheet)
    billboard_list = billboard[0].find_all('a')
    thread.start()
    thread.join()
    for single_billboard in billboard_list:
        music_param = single_billboard.attrs['href'].split('?')[1]
        sheet_name = single_billboard.get_text()
        result__sheet = result_workbook.add_sheet(str(sheet_name))
        thread = MyThread(music_param, result__sheet)
        thread.start()
        thread.join()
    result_workbook.save('E:/migu_music_result.xls')


begin_time = time.time()
startThread()
end_time = time.time()
print(end_time - begin_time)
