#!/usr/bin/env python
class Production(object):
    SQLALCHEMY_DATABASE_URI = "postgresql:///sports"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False
    GOOGLE_OAUTH2_CLIENT_ID = \
        '266875970319-r0so7u4a0qc2409s7t23v1fg4fa8gur5.apps.' +\
        'googleusercontent.com'
    GOOGLE_OAUTH2_CLIENT_SECRET = \
        'w2tdxisx2JkwKiOKg3ImFyRI'


class Development(object):
    SQLALCHEMY_DATABASE_URI = "postgresql:///sports"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    TESTING = False
    JSON_SORT_KEYS = False
    GOOGLE_OAUTH2_CLIENT_ID = \
        '266875970319-r0so7u4a0qc2409s7t23v1fg4fa8gur5.apps.' +\
        'googleusercontent.com'
    GOOGLE_OAUTH2_CLIENT_SECRET = 'w2tdxisx2JkwKiOKg3ImFyRI'
