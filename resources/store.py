from flask import Flask
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required

from models.store import StoreModel


class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
        type=str,
        required=True,
        help="Name of store"
    )

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {"message": "Store not found"}, 404


    def post(self, name):        
        if StoreModel.find_by_name(name):
            return {'message': f"A store with name '{name}' already exists"}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": f"Error in inserting store {name}"}, 500

        return store.json(), 201


    def delete(self, name):
        store = StoreModel.find_by_name(name)

        try:
            store.delete_from_db()
        except:
            return {"message": f"Error in deleting store {store.json()}"}, 500            

        return {'message': 'store deleted'}, 200


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}

