class Production(object):
    #SQLALCHEMY_DATABASE_URI = "postgresql://localhost/sports"
    DEBUG = False
    TESTING = False

class Development(object):
    #SQLALCHEMY_DATABASE_URI = "postgresql://localhost/sports"
    DEBUG = True 
    TESTING = False
