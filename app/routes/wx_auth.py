#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       pengj
    @   date    :       2019/12/30 18:44
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :
-------------------------------------------------
"""
from flask import Blueprint, request, jsonify
from wechatpy import WeChatClient

from config import load_config

__author__ = 'Max_Pengjb'

# 小程序配置信息
Config = load_config()

bp = Blueprint('xcc_auth', __name__, url_prefix="/wx/user")

wx_client = WeChatClient(appid=Config.XCC_APPID, secret=Config.XCC_SECRET)


# https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html
@bp.route("/login", methods=["POST", "GET"])
def get_json():
    data = request.get_json()
    code = data["code"]
    print(data)
    print(code)
    # 用code换取需要的access_token
    data2 = wx_client.wxa.code_to_session(code)
    # 调用上面方法，从返回的json数据里得到 对应数据 openid
    print(data2)
    print(type(data2))
    return jsonify(data2)
