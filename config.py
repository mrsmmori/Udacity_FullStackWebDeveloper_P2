#!/usr/bin/env python
import sys
sys.dont_write_bytecode = True


class Production(object):
    SQLALCHEMY_DATABASE_URI = "postgresql:///sports"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False
    GOOGLE_OAUTH2_CLIENT_ID = \
        '266875970319-72flnfnkmg9pg8njvb33dv58033g215h.apps.' +\
        'googleusercontent.com'
    GOOGLE_OAUTH2_CLIENT_SECRET = 'xSrQWexg8QgqY7c8WmBF2LhZ'


class Development(object):
    SQLALCHEMY_DATABASE_URI = "postgresql:///sports"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = False
    JSON_SORT_KEYS = False
    GOOGLE_OAUTH2_CLIENT_ID = \
        '266875970319-72flnfnkmg9pg8njvb33dv58033g215h.apps.' +\
        'googleusercontent.com'
    GOOGLE_OAUTH2_CLIENT_SECRET = 'xSrQWexg8QgqY7c8WmBF2LhZ'
