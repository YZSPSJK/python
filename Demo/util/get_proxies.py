# -*- coding:utf-8 -*-
import urllib
import xlwt
import time
from urllib import request, parse
import json
from bs4 import BeautifulSoup
import threading
import random


# 线程类
class MyThread(threading.Thread):
    def __init__(self, result__sheet):
        threading.Thread.__init__(self)
        self.result__sheet = result__sheet

    # 读取源文件xls 获取需要搜索的字符串
    def run(self):
        try:
            sheet = self.result__sheet
            for thread_index in range(0, 20):
                i = thread_index * 50 + 1
                fail_flag = False
                for request_time in range(0, 3):
                    soup = getHtml(thread_index + 1)
                    if soup != '':
                        break
                    if request_time == 2:
                        sheet.write(i, 0, '请求失败')
                        fail_flag = True
                    continue
                if not fail_flag:
                    ip_list = soup.find_all('tr', class_='odd')
                    for single_ip in ip_list:
                        single_info = single_ip.find_all('td')
                        if single_info[0].find('img') is None:
                            sheet.write(i, 0, '无国家')
                        else:
                            sheet.write(i, 0, single_info[0].find('img').attrs['alt'])
                        sheet.write(i, 1, single_info[1].string)
                        sheet.write(i, 2, single_info[2].string)
                        if single_info[3].find('a') is None:
                            sheet.write(i, 3, '无地址')
                        else:
                            sheet.write(i, 3, single_info[3].find('a').string)
                        sheet.write(i, 4, single_info[4].string)
                        sheet.write(i, 5, single_info[5].string.lower())
                        temp_speed = single_info[6].find('div', class_='bar_inner').attrs['style']
                        sheet.write(i, 6, temp_speed[temp_speed.index(':') + 1:temp_speed.index('%')])
                        connect_time = single_info[7].find('div', class_='bar_inner').attrs['style']
                        sheet.write(i, 7, connect_time[connect_time.index(':') + 1:connect_time.index('%')])
                        sheet.write(i, 8, single_info[8].string)
                        sheet.write(i, 9, single_info[9].string)
                        i += 1
                    time.sleep(3)
        except TypeError as e:
            print(e)
        except KeyError as e:
            print(e)


def getHtml(page_no):
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/' \
                     '537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
        headers = {'User-Agent': user_agent}
        url = 'http://www.xicidaili.com/nn/'
        url = url + str(page_no)
        req_res = request.Request(url, headers=headers)
        response_result = request.urlopen(req_res).read()
        content = response_result.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')
    except TypeError as e:
        print(e)
    except urllib.error.URLError as e:
        print(e)
        return ''
    return soup


# 启动线程
def get_proxies(result_file):
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('my proxies')
    sheet.write(0, 0, '国家')
    sheet.write(0, 1, 'IP地址')
    sheet.write(0, 2, '端口')
    sheet.write(0, 3, '服务器地址')
    sheet.write(0, 4, '类型')
    sheet.write(0, 5, '是否匿名')
    sheet.write(0, 6, '速度')
    sheet.write(0, 7, '连接时间')
    sheet.write(0, 8, '存活时间')
    sheet.write(0, 9, '验证时间')
    tsk = []
    for i in range(0, 1):
        temp_thread = MyThread(sheet)
        temp_thread.start()
        tsk.append(temp_thread)
    for tt in tsk:
        tt.join()
    workbook.save(result_file)


begin_time = time.time()
get_proxies('E:/music/proxies.xls')
end_time = time.time()
print(end_time - begin_time)
