import os

BASE_DIR = os.getcwd()
MODULE_DIR = os.path.join(os.getcwd(), 'app/modules/')
LOG_DIR = os.path.join(os.getcwd(), 'app/logs/')

class Config(object):
    JSON_AS_ASCII = False
    DEBUG = True
    TESTING = True
    SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'