# -*- coding: utf-8 -*-
import os
from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

# 官方文档 https://pythonhosted.org/Flask-Uploads/
'''
配置文件：FILES 需要替换为 UploadSet 实例的名称
UPLOADED_FILES_DEST : 设置文件存储的路径
UPLOADED_FILES_URL： 设置使用的服务器url， 末尾需要包含 /
UPLOADED_FILES_ALLOW：  设置允许上传的文件扩展名，其他被拒绝； 可以是 UploadSet 中定义以外的
UPLOADED_FILES_DENY： 设置禁止的文件扩展名

# 所有uploads实例公用的配置
UPLOADS_DEFAULT_DEST： 如果没有声明上传的文件地址,则会将文件存储到该地址内
UPLOADS_DEFAULT_URL： 网络服务器的url
'''


app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = r"/home/benny/视频/myFile-upload/"  # 文件储存地址

# 文件上传的实例，
# 可以使用 flask-uploads 自定义的多种文件格式
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)  # 绑定到 app中
patch_request_class(app, size=3 * 1024 * 1024)  # 文件大小限制，默认为16MB；本质还是通过设置 flask的配置 max_content_length

html = '''
    <!DOCTYPE html>
    <title>Upload File</title>
    <h1>图片上传</h1>
    <form method=post enctype=multipart/form-data>
         <input type=file name=photo>
         <input type=submit value=上传>
    </form>
    '''


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST' and 'photo' in request.files:
        # 使用实例的.save() 来存储文件 |  .path .url（） 来获取文件存储路径
        filename = photos.save(request.files['photo'])
        file_url = photos.url(filename)
        return html + '<br><img src=' + file_url + '>'
    return html


if __name__ == '__main__':
    app.run(port=5001, debug=True)
