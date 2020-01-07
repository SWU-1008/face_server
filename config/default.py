# coding: utf-8
import os


class Config(object):
    RESULT_ERROR = 0
    RESULT_SUCCESS = 1

    SITE = 'https://swu.mynatapp.cc/'
    JSON_AS_ASCII = False
    MONGODB_SETTINGS = {'ALIAS': 'default',
                        'DB': 'facepp',
                        'host': 'localhost',
                        'username': 'admin',
                        'password': ''}

    """Base config class."""
    # Flask app config
    DEBUG = True
    TESTING = True
    # token 的过期时间，7200 秒
    EXP_SECONDS = 7200

    # face小程序相关
    XCC_APPID = 'wx1aa81158cff54138'
    XCC_SECRET = '3feebc16725ad872ad430eaa9891b880'


    SECRET_KEY = "\xb5\xb3}#\xb7A\xcac\x9d0\xb6\x0f\x80z\x97\x00\x1e\xc0\xb8+\xe9)\xf0}"

    # Root path of project
    PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # 允许免登录的 url，不需要登录也可以访问
    allow_urls = ['/login',
                  '/register',
                  '/admin',
                  '/img/test',
                  '/img/img_upload',
                  '/img/img_download',
                  '/img/get_double_fold',
                  '/wx/user/login',
                  '/face/analyze'
                  ]

    # 允许上传的图片类型
    ALLOWED_IMAGE = {'png', 'jpg', 'jpeg', 'gif'}
