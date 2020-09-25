import os
import time
import hashlib
from pypinyin import lazy_pinyin


def allFile():
    path = ""
    # 获取文件夹下所有文件
    photoList = os.listdir(path)
    # 删除文件
    # 设置上传文件的字目录


# todo 文件名称处理
'''
why: 直接存储文件名称会造成安全问题
1. 使用Werkzeug secure_filename()函数处理文件名：
    **　只会返回ＡＳＣＩＩ字符，非ＡＳＣＩＩ字符会被过滤掉;
    **　需要将中文名称转化为英文, 使用 pypinyin 来转换
2. 统一处理非英文名称: 使用用户名的md5值作为文件夹的名称；使用 "用户名 + 时间戳"的md5值作为文件名
'''


def ChineseToPy(name):
    name, extension = name.split('.')
    newName = '_'.join(lazy_pinyin(name)) + '.' + extension
    return newName


def convertName(usrName):
    # python3中字符对象是unicode对象，不能直接加密
    # md5.update("123".encode("utf-8"))
    name = usrName.encode('utf-8')
    filePathName = hashlib.md5(name).hexdigest()[:15]
    fileName = (usrName + str(time.time())).encode('utf-8')
    fileName = hashlib.md5(fileName).hexdigest()[:32]
    return filePathName, fileName


def test():
    res = ChineseToPy("北京.jgp")
    print(f"{ChineseToPy.__name__}:", res)
    userName = "BennyJane"
    res = convertName(userName)
    print(res)


if __name__ == '__main__':
    test()
