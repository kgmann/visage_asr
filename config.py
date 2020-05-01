import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or ',\xd5\xc9YL\xe1\xea\xda3\xac\xf9)\x1c\xac\xa5\x7f'
    STORAGE_FOLDER = os.path.join(basedir, 'storage')
    UPLOAD_FOLDER = os.path.join(basedir, 'storage/uploads')
