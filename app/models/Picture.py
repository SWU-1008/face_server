#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------

    @   Author  :       pengj
    @   date    :       2019/12/8 14:44
    @   IDE     :       PyCharm
    @   GitHub  :       https://github.com/JackyPJB
    @   Contact :       pengjianbiao@hotmail.com
-------------------------------------------------
    Description :       
-------------------------------------------------
"""
import datetime

from app.models import db

__author__ = 'Max_Pengjb'


class Picture(db.Document):
    openid = db.StringField(max_length=255, verbose_name='小程序使用者的id')
    url = db.StringField(max_length=512, required=True, verbose_name='图url', unique=True)

    # 本地也保存的时候用，我们这里姑且保存一下吧
    image = db.ImageField(verbose_name='图片')
    origin_image_id = db.StringField(max_length=64, verbose_name='如果这张图是双眼皮，那这就保存双眼皮的原图')
    img_md5 = db.StringField(max_length=128, verbose_name='图片的md5唯一码，不要重复上传')
    img_type = db.StringField(max_length=64, verbose_name='图片type')
    create_time = db.DateTimeField(default=datetime.datetime.now, verbose_name='创建时间')

    def __unicode__(self):
        return self.img_name
