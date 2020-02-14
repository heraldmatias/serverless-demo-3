import os
import pymysql.cursors

class Config(object):
    MYSQL_DATABASE_HOST=os.getenv('MYSQLHOST', 'localhost')
    MYSQL_DATABASE_PORT= int(os.getenv('MYSQLPORT', 33061))
    MYSQL_DATABASE_USER=os.getenv('MYSQLUSER', 'root')
    MYSQL_DATABASE_PASSWORD=os.getenv('MYSQLPASS', '123456')
    MYSQL_DATABASE_DB=os.getenv('MYSQLDATABASE', 'singer')
    MYSQL_DATABASE_CHARSET=os.getenv('MYSQLENCODING', 'utf8')
    MYSQL_CURSOR_CLASS=pymysql.cursors.DictCursor
        
class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_DATABASE_HOST='localhost'
    MYSQL_DATABASE_PORT=33061
    MYSQL_DATABASE_USER='root'
    MYSQL_DATABASE_PASSWORD='123456'
    MYSQL_DATABASE_DB='singer'
    MYSQL_DATABASE_CHARSET='utf8'
    MYSQL_CURSOR_CLASS=pymysql.cursors.DictCursor
