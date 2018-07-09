# -*- coding:utf-8 -*-
import xlrd
import time
from xlutils.copy import copy
import random
from xpinyin import Pinyin
import threading


# 线程类
class MyThread(threading.Thread):
    def __init__(self, cell_index, result__sheet, source_sheet):
        threading.Thread.__init__(self)
        self.cell_index = cell_index
        self.result__sheet = result__sheet
        self.source_sheet = source_sheet

    # 读取源文件xls 获取需要搜索的字符串
    def run(self):
        try:
            for i in range(1 + self.cell_index * 1000, self.cell_index * 1000 + 1001):
                result__sheet = self.result__sheet
                source_sheet = self.source_sheet
                if source_sheet.cell(i, 0).ctype == 0:
                    continue
                song = source_sheet.cell(i, 3).value
                singer = source_sheet.cell(i, 4).value
                is_china = False
                for c in song:
                    if (65 <= ord(c) <= 90) or (97 <= ord(c) <= 122) or ord(c) == 32 or ord(
                            c) == 40 or ord(c) == 41:
                        pass
                    else:
                        is_china = True

                if is_china:
                    random_num = random.randint(1, 6)
                else:
                    random_num = random.randint(8, 10)
                change_result = change(song, singer, random_num)
                result__sheet.write(i, 5, change_result)
                result__sheet.write(i, 6, random_num)
        except TypeError as e:
            if hasattr(e, "code"):
                print(e.code)


# 启动线程
def startThread():
    source_workbook = xlrd.open_workbook('E:/song_singer_result.xls', formatting_info=True)
    result_workbook = copy(source_workbook)
    source_sheet = source_workbook.sheet_by_index(0)
    result_sheet = result_workbook.get_sheet(0)
    for i in range(0, 10):
        thread = MyThread(i, result_sheet, source_sheet)
        thread.start()
        thread.join()
    result_workbook.save('E:/song_singer_change_result.xls')


def change(song, singer, random_num):
    if random_num == 1:
        return change_form_one(song, singer)
    elif random_num == 2:
        return change_form_two(song, singer)
    elif random_num == 3:
        return change_form_three(song, singer)
    elif random_num == 4:
        return change_form_four(song, singer)
    elif random_num == 5:
        return change_form_five(song, singer)
    elif random_num == 6:
        return change_form_six(song, singer)
    elif random_num == 7:
        return change_form_seven(song, singer)
    elif random_num == 8:
        return change_form_eight(song, singer)
    elif random_num == 9:
        return change_form_nine(song, singer)
    elif random_num == 10:
        return change_form_ten(song, singer)
    else:
        return ''


def change_form_one(song, singer=None):
    reduce_word_num = 2
    if 1 <= len(song) <= 2:
        return song
    if 3 <= len(song) <= 5:
        reduce_word_num = 1
    num = random.randint(1, 3)
    if num == 1:
        return song[random.randint(1, reduce_word_num):len(song)]
    elif num == 2:
        middle_num = random.randint(1, len(song) - reduce_word_num - 1)
        return song[0:middle_num] + song[middle_num + random.randint(1, reduce_word_num):len(song)]
    elif num == 3:
        return song[0:len(song) - random.randint(1, reduce_word_num)]


def change_form_two(song, singer=None):
    insert_list = ['的', '得']
    insert_str = insert_list[random.randint(0, len(insert_list) - 1)]
    if len(song) == 1:
        return [insert_str + song, song + insert_str][random.randint(0, 1)]
    num = random.randint(1, 3)
    if num == 1:
        return insert_str + song
    elif num == 2:
        middle_num = random.randint(1, len(song) - 1)
        return song[0:middle_num] + insert_str + song[middle_num:len(song)]
    elif num == 3:
        return song + insert_str


def change_form_three(song, singer):
    connect_list = ['', ' ', '-', '+']
    connect_str = connect_list[random.randint(0, len(connect_list) - 1)]
    num = random.randint(1, 2)
    if num == 1:
        return song + connect_str * random.randint(1, 3) + singer
    elif num == 2:
        return singer + connect_str + song


def uncompleted_str(temp_str):
    if 0 <= len(temp_str) <= 1:
        return temp_str
    num = random.randint(1, 2)
    if num == 1:
        if temp_str.find(' ') == -1:
            return temp_str[0: random.randint(int(len(temp_str) / 2), len(temp_str) - 1)]
        else:
            blank_index_list = [i for i, x in enumerate(temp_str) if x == ' ']
            blank_random_index = blank_index_list[random.randint(0, len(blank_index_list)-1)]
            return [temp_str[0: blank_random_index], temp_str[blank_random_index + 1:len(temp_str)]][
                random.randint(0, 1)]
    elif num == 2:
        return temp_str[0: random.randint(int(len(temp_str) / 2), len(temp_str) - 1)]


def change_form_four(song, singer):
    connect_list = ['', ' ', '-', '+']
    connect_str = connect_list[random.randint(0, len(connect_list) - 1)]
    num = random.randint(1, 2)
    if num == 1:
        return change_form_one(song) + connect_str * random.randint(1, 3) + uncompleted_str(singer)
    elif num == 2:
        return uncompleted_str(singer) + connect_str + change_form_one(song)


def change_form_five(song, singer):
    connect_list = ['', ' ', '-', '+']
    connect_str = connect_list[random.randint(0, len(connect_list) - 1)]
    num = random.randint(1, 2)
    if num == 1:
        return change_form_two(song) + connect_str * random.randint(1, 3) + uncompleted_str(singer)
    elif num == 2:
        return uncompleted_str(singer) + connect_str + change_form_two(song)


def change_form_six(song, singer):
    p = Pinyin()
    connect_list = ['', ' ', '-']
    connect_str = connect_list[random.randint(0, len(connect_list) - 1)]
    return p.get_pinyin(song, connect_str)


def change_form_seven(song, singer):
    p = Pinyin()
    replace_time = random.randint(1, 3)
    temp_song = ''
    # for i in range(0, replace_time):
    #     replace_place = random.randint(0, len(song) - 1)
    #     replace_str = song[replace_place:replace_place + 1]
    #     p.get_pinyin(replace_str)
    #     replace_result_str = ''
    #     kvs = DefaultDagParams().get_phrase([p.get_pinyin(replace_str)], num=10)
    #     if len(kvs) > 0:
    #         while True:
    #             result_str = kvs[random.randint(0, len(kvs) - 1)][0]
    #             if result_str != replace_str:
    #                 replace_result_str = result_str
    #                 break
    #         temp_song = song[0:replace_place] + replace_result_str + song[replace_place + 1:len(song)]
    return temp_song


def change_form_eight(song, singer):
    connect_list = ['', ' ', '-', '+']
    connect_str = connect_list[random.randint(0, len(connect_list) - 1)]
    num = random.randint(1, 2)
    if num == 1:
        return song + connect_str * random.randint(1, 3) + uncompleted_str(singer)
    elif num == 2:
        return uncompleted_str(singer) + connect_str + song


def change_form_nine(song, singer):
    return uncompleted_str(song)


def change_form_ten(song, singer):
    return [song.lower(), song.capitalize()][random.randint(0, 1)] + " " + [singer.lower(), singer.capitalize()][
        random.randint(0, 1)]


begin_time = time.time()
# start()
startThread()
end_time = time.time()
print(end_time - begin_time)
