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
class SearchThread(threading.Thread):
    def __init__(self, thread_index, result__sheet, temp_list):
        threading.Thread.__init__(self)
        self.thread_index = thread_index
        self.result__sheet = result__sheet
        self.temp_list = temp_list

    # 读取源文件xls 获取需要搜索的字符串
    def run(self):
        # try:
        result__sheet = self.result__sheet
        temp_list = self.temp_list
        thread_index = self.thread_index
        i = thread_index * 625 + 1
        for search_word in temp_list:
            if isinstance(search_word, float) or isinstance(search_word, int):
                search_word = int(search_word)
            search_word = 'When It All Falls Down'
            songdictlist = []
            songdictlist.append(getMiGuDictByWord(search_word))
            songdictlist.append(getDogDictByWord(search_word))
            songdictlist.append(getXiaMiDictByWord(search_word))
            songdictlist.append(getQQDictByWord(search_word))
            songdictlist.append(getCloudDictByWord(search_word))
            expected_result = get_expected_word(songdictlist)
            print(expected_result)
            expected_song = expected_result[0: expected_result.index('-')]
            expected_singer = expected_result[expected_result.index('-') + 1: len(expected_result)]
            result__sheet.write(i, 2, expected_song)
            result__sheet.write(i, 3, expected_singer)
            start_index = 5
            for songdict in songdictlist:
                if len(songdict) <= 0:
                    result__sheet.write(i, start_index, 0)
                    start_index += 1
                    continue
                index_for_expected_song = 1
                for singlesonginfo in songdict:
                    if (singlesonginfo.get('song') + '-' + singlesonginfo.get('singer')) != expected_result:
                        index_for_expected_song += 1
                        continue
                    result__sheet.write(i, start_index, index_for_expected_song)
                    break
                start_index += 1
            i += 1
            # except TypeError as e:
            #     print(e)


def get_expected_word(templist):
    temp_dict = {}
    num = 1
    result = templist[0][0].get('song') + '-' + templist[0][0].get('singer')
    for singlesongdict in templist:
        if len(singlesongdict) <= 0:
            continue
        tempstr = singlesongdict[0].get('song') + '-' + singlesongdict[0].get('singer')
        if temp_dict.get(tempstr) is None:
            temp_dict[tempstr] = 1
        else:
            temp_dict[tempstr] = temp_dict.get(tempstr) + 1
    for key, value in temp_dict.items():
        if value > num:
            num = value
            result = key
    return result


# 启动线程
def startThread(source_file, result_file):
    source_xls = xlrd.open_workbook(source_file, formatting_info=True)
    result_xls = copy(source_xls)
    source_sheet = source_xls.sheet_by_index(0)
    result__sheet = result_xls.get_sheet(0)
    result__sheet.write(0, 2, '歌曲名称')
    result__sheet.write(0, 3, '歌手名称')
    result__sheet.write(0, 5, '咪咕')
    result__sheet.write(0, 6, '酷狗')
    result__sheet.write(0, 7, '虾米')
    result__sheet.write(0, 8, 'QQ')
    result__sheet.write(0, 9, '网易云音乐')

    tsk = []
    for i in range(0, 1):
        temp_list = []
        for j in range(i * 625, i * 625 + 625):
            if j > 100:
                break
            if source_sheet.cell(j, 0).ctype == 0:
                continue
            temp_list.append(source_sheet.cell(j, 0).value)
        temp_thread = SearchThread(i, result__sheet, temp_list)
        temp_thread.start()
        tsk.append(temp_thread)
    for tt in tsk:
        tt.join()
    result_xls.save(result_file)


begin_time = time.time()
startThread('E:/hot_word_one.xls', 'E:/hot_word_result.xls')
end_time = time.time()
print(end_time - begin_time)
