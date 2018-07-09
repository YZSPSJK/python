# -*- coding:utf-8 -*-
import xlrd
import time
from xlutils.copy import copy
import threading
from cloud.searchCloudByWord import getCloudDictByWord
from qq.searchQQByWord import getQQDictByWord
from cool_dog.searchDogByword import getDogDictByWord
from migu.searchMiguByWord import getMiGuDictByWord
from xiami.searchXIamiByWord import getXiaMiDictByWord


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
                songdictlist = []
                songdictlist.append(getCloudDictByWord(search_word))
                songdictlist.append(getDogDictByWord(search_word))
                songdictlist.append(getXiaMiDictByWord(search_word))
                songdictlist.append(getMiGuDictByWord(search_word))
                songdictlist.append(getQQDictByWord(search_word))
                for singlesongdict in songdictlist:
                    pass
        except TypeError as e:
            print(e)


# 启动线程
def startThread(source_file, result_file):
    source_xls = xlrd.open_workbook(source_file, formatting_info=True)
    result_xls = copy(source_xls)
    source_sheet = source_xls.sheet_by_index(0)
    result__sheet = result_xls.get_sheet(0)
    result__sheet.write(0, 2, '歌曲名称')
    result__sheet.write(0, 3, '歌手名称')

    tsk = []
    for i in range(0, 1):
        temp_list = []
        for j in range(i * 625, i * 625 + 625):
            if j > 10000:
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


begin_time = time.time()
print(1)
startThread('E:/hot_word_one.xls', 'E:/hot_word_result.xls')
end_time = time.time()
print(end_time - begin_time)
