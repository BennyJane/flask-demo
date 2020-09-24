# -*- coding: utf-8 -*-
import os
from flask import Flask, request
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

app = Flask(__name__)
app.config['UPLOADED_PHOTOS_DEST'] = r"/home/benny/视频/myFile-upload/"  # 文件储存地址

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
        filename = photos.save(request.files['photo'])
        file_url = photos.url(filename)
        return html + '<br><img src=' + file_url + '>'
    return html


if __name__ == '__main__':
    app.run(port=5001, debug=True)
