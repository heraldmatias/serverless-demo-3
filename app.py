import logging
import os
from collections import namedtuple
from random import choice

from flask import Flask, json, request
# Import the X-Ray modules
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware
from aws_xray_sdk.core import patcher, xray_recorder, patch_all

from mysql import SingerMysql

Quote = namedtuple("Quote", ("text", "author"))
env = os.getenv('ENVIRONMENT')

quotes = [
    Quote("Talk is cheap. Show me the code.", "Linus Torvalds"),
    Quote("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    Quote("Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live",
          "John Woods"),
    Quote("Give a man a program, frustrate him for a day. Teach a man to program, frustrate him for a lifetime.", "Muhammad Waseem"),
    Quote("Progress is possible only if we train ourselves to think about programs without thinking of them as pieces of executable code. ",
          "Edsger W. Dijkstra")
]

# Patch the requests module to enable automatic instrumentation
# patcher.patch(('SingerMysql',))

app = Flask(__name__)

# Configure the X-Ray recorder to generate segments with our service name
#plugins = ('EC2Plugin', )
xray_recorder.configure(service='Quotes Serverless App') #, plugins=plugins)
#patch_all()
# Instrument the Flask application
XRayMiddleware(app, xray_recorder)

#config
if env == 'PRODUCTION':
  app.config.from_object('config.ProductionConfig')
else:
  app.config.from_object('config.DevelopmentConfig')

# logging
logging.basicConfig(level='WARNING')
logging.getLogger('aws_xray_sdk').setLevel(logging.DEBUG)
logger = logging.getLogger('aws_xray_sdk')

# mysql
mysql = SingerMysql()
mysql.init_app(app)

@app.route("/quote", methods=["GET"])
def get_random_quote():
    return json.jsonify(choice(quotes)._asdict())

@xray_recorder.capture('## create_movie')
@app.route("/movies", methods=["POST"])
def create_movie():
    xray_log('config data', app.config)
    con = mysql.get_db()
    cursor = con.cursor()

    #cursor.execute("""create table if not exists movie(title varchar(30) , directors varchar(200) , catagory varchar(30)  , rating int) """)
    data = json.loads(request.data)
    xray_log('task', 'saving data %s ' % request.data)    
    cursor.execute("""insert into movie values(%s, %s, %s,%s) """, 
    (data.get('title'), data.get('directors'),data.get('category'), data.get('rating'),) )
    con.commit()

    return json.jsonify({'success': True})

@xray_recorder.capture('## get_movies')
@app.route("/movies", methods=["GET"])
def get_movies():
    cursor = mysql.get_db().cursor()
    cursor.execute(""" select * from movie """)
    data = cursor.fetchall()
    xray_log('task', 'getting all movies')
    return json.jsonify(data)

def xray_log(action, message):
  if xray_recorder.current_subsegment():
      xray_recorder.current_subsegment().put_metadata(action, message)

