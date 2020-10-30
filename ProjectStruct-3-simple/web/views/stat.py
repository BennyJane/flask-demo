from flask import Blueprint, render_template

# 数据处理的核心功能部分
stat_bp = Blueprint('stat', __name__)


@stat_bp.route('/')
def index():
    return "<h1>数据处理接口</h1>"
