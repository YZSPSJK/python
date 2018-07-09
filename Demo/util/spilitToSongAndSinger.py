# -*- coding:utf-8 -*-
import urllib
import xlrd
import time
from urllib import request, parse
import json
from xlutils.copy import copy
import threading


def start():
    source_workbook = xlrd.open_workbook('E:/song_singer.xls', formatting_info=True)
    result_workbook = copy(source_workbook)
    source_sheet = source_workbook.sheet_by_index(0)
    result_sheet = result_workbook.get_sheet(0)

    for i in range(1, 10001):
        if source_sheet.cell(i, 0).ctype == 0:
            continue
        song_singer = source_sheet.cell(i, 0).value
        song = song_singer[0:song_singer.index('++')]
        singer = song_singer[song_singer.index('++')+2:len(song_singer)]
        result_sheet.write(i, 3, song)
        result_sheet.write(i, 4, singer)
    result_workbook.save('E:/song_singer_result.xls')


begin_time = time.time()
start()
end_time = time.time()
print(end_time - begin_time)
