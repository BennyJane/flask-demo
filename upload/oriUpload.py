import os, sys
from flask import Flask, request, jsonify, Response, redirect, url_for, send_from_directory
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.wsgi import responder
from werkzeug.utils import secure_filename  # 获取上传文件的文件名

app = Flask(__name__)

UPLOAD_FOLDER = r"/home/benny/视频/myFile-upload/"
ALLOW_EXTENSIONS = ('txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # 保存入config 全局变量, 确保在各个位置都可以访问
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # FIXME 利用Flask自身的配置限制上传文件的大小；异常无法捕获


def allow_file_type(filename):
    # 1.文件名称必须带 '.'
    # 2.文件的扩展名必须是被允许的扩展名称
    return '.' in filename and filename.split('.', 1)[1] in ALLOW_EXTENSIONS


@app.errorhandler(413)
def globalError(e):
    # todo 无法捕获该错误
    # 文件大小超过设置的限制的时候, 触发 RequestEntityTooLarge；状态码 413
    if isinstance(e, RequestEntityTooLarge):
        print(e)
    errorMsg = sys.exc_info()
    message = str(errorMsg[1])
    print('error', message)
    return 'file is too large !!'


@app.route('/', methods=['get', 'post'])
def upload_file():
    print('upload_file ...')
    if request.method == 'POST':
        file = request.files['file']
        # print('upload_file ...1')
        fileName = file.filename
        if file and allow_file_type(fileName):  # 限制文件类型
            fileName = secure_filename(fileName)
            savedPath = os.path.join(UPLOAD_FOLDER, fileName)
            file.save(savedPath)  # 保存文件
            # print(file)
            # fixme 限制文件大小, 先将文件保存后,再获取文件大小
            fileSize = round(os.path.getsize(savedPath) / 1024 / 1204, 3)
            unit = 'MB'
            if fileSize == 0:
                fileSize = round(os.path.getsize(savedPath) / 1024, 3)
                unit = 'KB'
            print(sys.getsizeof(file))  # todo 不明白该含义
            return f'{fileName} success! file size is {fileSize}{unit}'
    return '''
        <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<filename>')
def getFile(filename):
    # 传入两个参数: 文件夹名称, 文件名
    return send_from_directory(UPLOAD_FOLDER, filename)


if __name__ == '__main__':
    app.run(debug=True)

'''
参考文章: 
werkzeug的报错 RequestEntityTooLarge, 使用flask的异常捕获,不能捕获该错误, 线上生产可能会直接断开链接
https://werkzeug.palletsprojects.com/en/1.0.x/exceptions/#werkzeug.exceptions.RequestEntityTooLarge


总结: 
** 同名文件不会重复上传!

'''
