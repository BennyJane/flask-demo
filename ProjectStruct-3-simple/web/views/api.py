from flask import Blueprint
from flask import jsonify

from web.utils.response import ReqJson

api_bp = Blueprint('api', __name__)


@api_bp.route('/')
def index():
    res = ReqJson(code=0)
    res.msg = "API接口"
    return res.result
