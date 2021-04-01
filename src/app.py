from flask import Flask
from flask_restful import Api
from database.db import initialize_db
from routers.routes import initialize_routes
from pymongo import ReadPreference

import log
logger = log.setup_custom_logger('root')
logger.debug('main message')


app = Flask(__name__)
# app.config['MONGODB_DB'] = 'english_db'
# app.config['MONGODB_HOST'] = 'mongodb://catalog:123456@127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019,127.0.0.1:27020/?authSource=admin&replicaSet=rs0&readPreference=primary&appname=MongoDB%20Compass&ssl=false'
api = Api(app)
app.config['MONGODB_SETTINGS'] = {
    'host': "mongodb://catalog:123456@127.0.0.1:27017,127.0.0.1:27018,127.0.0.1:27019,127.0.0.1:27020/english_db",
    'replicaSet': 'rs0',
    'read_preference': ReadPreference.SECONDARY_PREFERRED
}


initialize_db(app)
initialize_routes(api)

if __name__ == '__main__':
    app.run()
