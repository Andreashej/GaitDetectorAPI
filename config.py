import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you_will_never_guess'

    DB_USERNAME = 'andreas2_gaitdetection'
    DB_PASSWORD = 'wH*miIi?E+1!'
    DB_NAME = 'andreas2_gaitdetection'
    DB_PORT = '3306'
    DB_HOSTNAME = 'cp02.azehosting.net'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOSTNAME + ':' + DB_PORT + '/' + DB_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = False