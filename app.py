import os

from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager

from resources.item import Item, ItemList
from resources.user import Login, UserRegister
from resources.store import Store, StoreList


app = Flask(__name__)
db_uri = os.environ.get('DATABASE_URL','sqlight:///data.db')
# Handle deprecated heroku uri ('postgres://' -> 'postgresql://')
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'
api = Api(app)

jwt = JWTManager(app)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Login, '/auth')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)


