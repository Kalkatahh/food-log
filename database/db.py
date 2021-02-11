from flask import Flask, render_template, request, url_for, make_response, jsonify, session, Blueprint
from flask_sqlalchemy import SQLAlchemy
import asyncio
database = Blueprint('db', __name__)
app = None
db = None
users = None
pantry = None


class Database:
    def __init__(self, application, app_db):
        global app, db, users, pantry
        app = application
        db = app_db

        users = self.create_users_tables()
        pantry = self.create_pantry_tables()

    def create_users_tables(self):
        class Users(db.Model):
            __tablename__ = 'Users'
            id = db.Column(db.Integer, primary_key=True)
            username = db.Column(db.String(200), unique=True)
            password = db.Column(db.String(200))

            def __init__(self, username, password):
                self.username = username
                self.password = password
        return Users

    def create_pantry_tables(self):
        class Pantry(db.Model):
            __tablename__ = 'Food'
            id = db.Column(db.Integer, primary_key=True)
            code = db.Column(db.String(200), unique=True)
            name = db.Column(db.String(200))
            count = db.Column(db.Integer)
            # user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))

            def __init__(self, code, name, count):
                self.code = code
                self.name = name
                self.count = count
                # self.user_id = user_id
        return Pantry
        # users = Users
        # pantry = Pantry
        #print('after', users, pantry)

    def get_users_table(self):
        return users

    def get_pantry_table(self):
        return pantry

    def get_db_object(self):
        return db
