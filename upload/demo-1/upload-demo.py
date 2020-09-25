import os
import random

from PIL import Image
from flask import Flask, render_template
from flask_uploads import UploadSet, IMAGES, patch_request_class, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed, FileField
from wtforms import SubmitField

# 需要加s templates
app = Flask(__name__, static_folder=r'./templates')

'''
==========================  配置文件上传模块
'''
photos = UploadSet("photos", IMAGES)
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(os.getcwd(), 'uploads')
# app.config["UPLOADEd_PHOTOS_URL"] = ''
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
configure_uploads(app, photos)
patch_request_class(app, size=None)

'''
==========================  添加表单
'''
app.config["SECRET_KEY"] = "BENNYJANE"


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileRequired(message="未选择文件"), FileAllowed(photos, message="只能上传图片")])
    submit = SubmitField("上传")


def random_string(length=32):
    # fixme 优化
    base_str = 'qwertyuioplkjhgfdsazcxvbnm0123456789'
    return ''.join(random.choice(base_str) for _ in range(length))


# 生成缩略图并保存
def Thumbnail(path):
    img = Image.open(path)
    img.thumbnail((128, 128))
    path, filename = os.path.split(path)
    print(filename)
    name =filename[:5] + '_thumbnail.jpg'
    newPath = os.path.join(path, name)
    img.save(newPath)


@app.route('/upload/', methods=['get', 'post'])
def upload():
    img_url = None
    form = UploadForm()
    if form.validate_on_submit():
        image = form.photo.data
        if not image:
            return
        print(form.photo.data.filename)
        suffix = os.path.split(form.photo.data.filename)[1]
        filename = random_string() + suffix
        # subFolder: 子目录  name： 文件名称
        photos.save(image, name=filename)
        # 需要传入文件保存的名称
        img_url = photos.url(filename)
        # print(img_url)
        # print(photos.path(filename))
        # 生成缩略图
        savedPath = photos.path(filename)
        Thumbnail(savedPath)
    return render_template('upload.html', form=form, img_url=img_url)


if __name__ == '__main__':
    app.run(debug=True)
