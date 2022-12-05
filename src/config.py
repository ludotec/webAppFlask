class Config():
    SECRET_KEY = 'B!1weNAt1T^%kvhUI*^'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_DATABASE_HOST = 'localhost'
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_PASSWORD = ''
    MYSQL_DATABASE_DB = 'login_example'

config = {
    'development': DevelopmentConfig
}