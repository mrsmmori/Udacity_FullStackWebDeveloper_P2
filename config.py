class Production(object):
    #SQLALCHEMY_DATABASE_URI = "postgresql://localhost/sports"
    DEBUG = False
    TESTING = False
    JSON_SORT_KEYS = False

class Development(object):
    #SQLALCHEMY_DATABASE_URI = "postgresql://localhost/sports"
    DEBUG = True 
    TESTING = False
    JSON_SORT_KEYS = False
