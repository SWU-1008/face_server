#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       pengj
    @   date    :       2019/12/31 16:40
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""
from flask import Blueprint, jsonify, request

__author__ = 'Max_Pengjb'

from PythonSDK.facepp import API

# 初始化对象，进行api的调用工作
api = API()

__author__ = 'Max_Pengjb'

# 融合图片，这是一个有双眼皮的人
# merge_url = 'https://cdn.faceplusplus.com.cn/mc-official/scripts/demoScript/images/demo-pic114.jpg'
merge_url = 'https://i.loli.net/2019/12/31/CWGY1yiPcKeXRgh.jpg'
# 这是没有双眼皮的人
# template_url = 'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1574981557927&di=484eae05e3ed0c0f4d30914862a012a0&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fimages%2F20181110%2F2063daae7ad94d3294d21fda4d604a6b.jpeg'
template_url = 'https://i.loli.net/2019/12/31/QGaV9YOPmMHle13.jpg'

bp = Blueprint('face', __name__, url_prefix="/face")


@bp.route("/analyze", methods=['GET', 'POST'])
def analyze():
    req_json = request.json
    if not req_json or not req_json.get('faceUrl'):
        return jsonify({'error_message': '请上传faceUrl照片地址'})
    image_url = req_json.get('faceUrl')
    # 面部特征分析API https://console.faceplusplus.com.cn/documents/118131136
    # return_imagereset 是否返回人脸矫正后图片。合法值为：0不返回 1返回 注：本参数默认值为 0
    facepp_feature_res = api.facialfeatures(image_url=image_url)
    return jsonify(facepp_feature_res.result)
