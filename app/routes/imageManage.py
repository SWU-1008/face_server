#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       pengj
    @   date    :       2019/12/8 14:27
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""
from qcloud_cos import CosConfig, CosS3Client, CosServiceError

__author__ = 'Max_Pengjb'
import base64
import io
import hashlib
from bson import ObjectId
from flask import Blueprint, send_file, request, Response
from app import jsonReturn
from app.models.Picture import Picture
from config import load_config

# 对象存储的信息
Config = load_config()
# 2. 获取客户端对象

bp = Blueprint('image', __name__, url_prefix="/img")


@bp.route('/test')
def get_blank():
    gif = 'R0lGODlhAQABAIAAAP///////yH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=='
    gif_str = base64.b64decode(gif)
    return send_file(io.BytesIO(gif_str), mimetype='image/gif')


@bp.route('/get_double_fold', methods=['GET', 'POST'])
def get_double_fold():
    req_json = request.json
    if not req_json:
        return jsonReturn.falseReturn(request.path, '请传必要参数')
    origin_img_id = req_json.get('originImgId')
    open_id = req_json.get('openId')
    if not all([origin_img_id is not None, open_id is not None]):
        return jsonReturn.falseReturn(request.path, '请传必要参数')
    pic = Picture.objects(openid=open_id, origin_image_id=origin_img_id).first()
    if pic:
        return jsonReturn.trueReturn({'imgId': str(pic.id)}, 'ok')
    else:
        return jsonReturn.falseReturn('', '还没搞好')


# 上传图片，我们这里使用 微信对象存储（sm.ms 图床太垃圾了），把传回来的 url 保存在mongodb中
# element ui 的上传图片
@bp.route("/img_upload", methods=['POST'])
def img_upload():
    req_args = request.form
    print(req_args)
    if not req_args:
        return jsonReturn.falseReturn(request.path, '请传必要参数')
    open_id = req_args.get('openId')
    if open_id is None:
        return jsonReturn.falseReturn(request.path, '请传必要参数')
    if 'img' not in request.files:
        return jsonReturn.falseReturn(request.path, '请上传file文件')
    img_obj = request.files.get("img")
    filename = img_obj.filename
    if not filename:
        return jsonReturn.falseReturn(request.path, '请上传file文件')
    img_type = filename[filename.rfind(".") + 1:].lower()
    # print(img_type)
    # pic = Picture(image=img_obj)
    if img_type in Config.ALLOWED_IMAGE:
        try:
            file_MD5 = hashlib.md5(img_obj.read()).hexdigest()
            img_url = Config.SITE + file_MD5
            pic = Picture.objects(img_md5=file_MD5).first()
            if pic:
                return jsonReturn.trueReturn({'imgId': str(pic.id)}, '该文件已经存在了')
            img_obj.seek(0)  # 前面计算 md5 的时候已经 read(） 一次了，这里要再读取一次，需要把游标归 0
            # 保存图片到 mongodb 的 picture 中
            pic = Picture(img_md5=file_MD5, url=img_url, openid=open_id)
            pic.image.put(img_obj)
            pic.save()
            return jsonReturn.trueReturn({'imgId': str(pic.id)}, '上传成功')
        except CosServiceError as e:
            return jsonReturn.falseReturn(e.get_error_msg(), '上传失败')
        except Exception as e:
            return jsonReturn.falseReturn('', '上传失败 ' + str(e))
    else:
        return jsonReturn.falseReturn(request.path, '格式不对，仅支持： ' + str(Config.ALLOWED_IMAGE))


@bp.route("/img_download", methods=['GET'])
def img_download():
    req_args = request.args
    if not req_args:
        return jsonReturn.falseReturn(request.path, '请传必要参数')
    img_id = req_args.get('imgId')
    if img_id is None:
        return jsonReturn.falseReturn(request.path, '请传必要参数')
    pic = Picture.objects.get(id=ObjectId(img_id))
    # 获取 头像 的 ImageGridFsProxy
    image_gfs_proxy = pic.image
    print(image_gfs_proxy.content_type)
    print(image_gfs_proxy)
    return Response(image_gfs_proxy.read(),
                    content_type="image/jpeg",
                    headers={
                        'Content-Length': image_gfs_proxy.length
                    })


# 上面那个是需要传参的下载图片，把图片参数直接写到url里面，形成类似图床的效果（由于对路径的权限控制，这里不太好，所以要是建议用上面的）
@bp.route("/img_download_ui/<img_id>", methods=['GET', 'POST'])
def img_download_ui(img_id):
    pic = Picture.objects.get(id=ObjectId(img_id))
    # 获取 头像 的 ImageGridFsProxy
    image_gfs_proxy = pic.image
    print(image_gfs_proxy.content_type)
    print(image_gfs_proxy)
    return Response(image_gfs_proxy.read(),
                    content_type="image/jpeg",
                    headers={
                        'Content-Length': image_gfs_proxy.length
                    })
