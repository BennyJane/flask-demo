from flask import Blueprint, render_template

api_bp = Blueprint('api', __name__)


@api_bp.route('/')
def index():
    return "<h1> 数据上传接口 </h1>"
