# !/usr/bin/env python
# -*-coding:utf-8 -*-
# Warning    ：The Hard Way Is Easier
from flask import jsonify
from webApp.apis.v1 import api_bp_v1
from webApp.errors.api_exception import RspJson


@api_bp_v1.route("/index")
def index():
    rep = RspJson(
        code=0,
        data={
            "project": "standard project",
            "version": "0.1.0",
            "create_at": "20210109",
            "author": "benny jane"
        },
        msg="")
    return jsonify(rep.result)
