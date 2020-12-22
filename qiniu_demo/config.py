#encoding: utf-8
import os

print(__file__)
print(os.path.dirname(__file__))

UEDITOR_UPLOAD_PATH = os.path.join(os.path.dirname(__file__),'images')

UEDITOR_UPLOAD_TO_QINIU = True
UEDITOR_QINIU_ACCESS_KEY = "NaTF79Ps5Gx4Ee8LcuhViZHMZQL9ow-tNA-5hwAQ"
UEDITOR_QINIU_SECRET_KEY = "jjRQRitfFrWoUGfS8rj-sP57mkzhJvshL0rKeMSi"
UEDITOR_QINIU_BUCKET_NAME = "myfile02-public"
UEDITOR_QINIU_DOMAIN = "http://cdn.img.pygorun.com/"


FLASK_ENV='development'
