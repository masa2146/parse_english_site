from flask_mongoengine import MongoEngine
from mongoengine import connect
from mongoengine import connect
from pymongo import ReadPreference
db = MongoEngine()

def initialize_db(app):

    connect('english_db', host='mongodb://catalog:123456@127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019,127.0.0.1:27020/?authSource=admin&replicaSet=rs0&readPreference=secondaryPreferred&appname=MongoDB%20Compass&ssl=false', read_preference=ReadPreference.SECONDARY_PREFERRED)
    # db.init_app(app)
