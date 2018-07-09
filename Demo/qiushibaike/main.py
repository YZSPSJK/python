from test import catch
import os
import datetime
import json


def writeToTxt(list_name, file_path):
    try:
        fp = open(file_path, 'w+', encoding='utf-8')
        l = len(list_name)
        i = 0
        fp.write('[')
        for item in list_name:
            fp.write(json.dumps(item))
            if i < l - 1:
                fp.write(',\n')
            i += 1
        fp.write(']')
        fp.close()
    except IOError:
        print('fail to open file')


def saveBlogs():
    for i in range(1, 2):
        print('request for' + str(i) + '...')
        blogs = catch.blogParser(i)
        path = createFile()
        writeToTxt(blogs, path + '/blog_' + str(i) + '.json')
        print('the ' + str(i) + '  finished')
    return 'success'


def createFile():
    date = datetime.datetime.now().strftime('%Y-%m-%d')
    path = 'E:/' + date
    if os.path.exists(path):
        return path
    else:
        os.mkdir(path)
        return path


result = saveBlogs()
print(result)
