# -*- coding:utf-8 -*-
import urllib
import xlrd
import time
from urllib import request, parse
import json
from xlutils.copy import copy
import threading
import random
from bs4 import BeautifulSoup


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
            i = thread_index * 625
            for search_word in temp_list:
                if isinstance(search_word, float) or isinstance(search_word, int):
                    search_word = int(search_word)
                print(search_word)
                fail_flag = False
                for request_time in range(0, 3):
                    response = getHtml(search_word)
                    if response != '':
                        break
                    if request_time == 2:
                        result__sheet.write(i, 3, '请求失败')
                        i += 1
                        fail_flag = True
                    continue
                if fail_flag:
                    continue
                song_soup = response.find_all('table', class_='track_list')[0]
                song_list_soup = song_soup.find_all('tr')
                singer = ''
                singer_list_soup = song_soup.find_all('tr')[1].find('td', class_='song_artist').find_all('a')
                if len(singer_list_soup) > 1:
                    for single_singer in singer_list_soup:
                        singer = singer + single_singer.attrs['title'] + '&'
                    singer = singer[0:len(singer) - 1]
                else:
                    singer = singer_list_soup[0].attrs['title']
                result__sheet.write(i, 3,
                                    song_soup.find_all('tr')[1].find('td', class_='song_name').find('a').attrs[
                                        'title'])
                result__sheet.write(i, 4, singer)
                result__sheet.write(i, 5,
                                    song_soup.find_all('tr')[1].find('td', class_='song_album').find('a').attrs[
                                        'title'])
                i = i + 1
                time.sleep(random.uniform(0.2, 1.5))
        except TypeError as e:
            print(e)
        except KeyError as e:
            print(e)


def getHtml(search_word):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/' \
                     '537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
        headers = {'User-Agent': user_agent}
        url = 'https://www.xiami.com/search?key=' + parse.quote(str(search_word))+'&pos=1'
        req_res = request.Request(url, headers=headers)
        response_result = request.urlopen(req_res).read()
        response_json = response_result.decode('utf-8')
        soup = BeautifulSoup(response_json, 'html.parser')
    except TypeError as e:
        print(e)
    except urllib.error.URLError as e:
        print(e)
        return ''
    except UnicodeDecodeError as e:
        print(e)
        return ''
    return soup


def getProxies():
    work_book = xlrd.open_workbook('E:/music/proxies.xls', formatting_info=True)
    source_sheet = work_book.sheet_by_index(0)
    temp_list = []
    for i in range(1, 10001):
        if source_sheet.cell(i, 1).ctype == 0:
            continue
        if source_sheet.cell(i, 2).ctype == 0:
            continue
        if source_sheet.cell(i, 5).ctype == 0:
            continue
        single_proxy = source_sheet.cell(i, 5).value + '://' + source_sheet.cell(i, 1).value + ':' + source_sheet.cell(
            i, 2).value
        temp_list.append(single_proxy)
    return temp_list


# 启动线程
def startThread(source_file, result_file):
    source_xls = xlrd.open_workbook(source_file, formatting_info=True)
    result_xls = copy(source_xls)
    source_sheet = source_xls.sheet_by_index(0)
    result__sheet = result_xls.get_sheet(0)

    tsk = []
    for i in range(0, 16):
        temp_list = []
        for j in range(i * 625, i * 625 + 625):
            if source_sheet.cell(j, 0).ctype == 0:
                continue
            temp_list.append(source_sheet.cell(j, 0).value)
        temp_thread = MyThread(i, result__sheet, temp_list)
        temp_thread.start()
        tsk.append(temp_thread)
    for tt in tsk:
        tt.join()
    result_xls.save(result_file)


def getXiaMiDictByWord(search_word):
    result_list = []
    for request_time in range(0, 3):
        response = getHtml(search_word)
        if response != '':
            break
        if request_time == 2:
            return result_list
            i += 1
        continue
    song_soup = response.find_all('table', class_='track_list')[0]
    song_list_soup = song_soup.find_all('tr')
    i = 0
    for each_song in song_list_soup:
        i += 1
        if i == 1:
            continue
        if i > 21:
            break
        each_song_info = {}
        singer = ''
        singer_list_soup = each_song.find('td', class_='song_artist').find_all('a')
        if len(singer_list_soup) > 1:
            ingoreflag = True
            for single_singer in singer_list_soup:
                if ingoreflag:
                    ingoreflag = False
                    continue
                singer = singer + single_singer.text + '&'
            singer = singer[0:len(singer) - 1]
        else:
            singer = singer_list_soup[0].attrs['title']
        each_song_info['song'] = each_song.find('td', class_='song_name').find('a', target='_blank').text
        each_song_info['singer'] = singer
        result_list.append(each_song_info)
        # each_song_info['album'] = song_list_soup[i].find('td', class_='song_album').find('a').attrs['title']
    # time.sleep(random.uniform(0.2, 1.5))
    return result_list


# print(getXiaMiDictByWord('镇魂'))
# begin_time = time.time()
# startThread('E:/music/hot_word_one.xls', 'E:/hot_word_one_cloud.xls')
# end_time = time.time()
# print(end_time - begin_time)
