import config  # create your own config.py with variables
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api.api_routes import api, setup_api_db
from view.routes import view, setup_view_db
from database.db import Database
app = Flask(__name__)
app.secret_key = config.secret_key
ENV = config.env

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = config.local_db
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = config.heroku_db

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# TODO fix so that instead of passing in db I can get it from db.py
app.register_blueprint(api)
app.register_blueprint(view)
database = Database(app, db)
app.config["db"] = database
app.config["api.db"] = setup_api_db(db, database)


if __name__ == '__main__':
    app.run()
