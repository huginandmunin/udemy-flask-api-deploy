from flask import Flask
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required

from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="Price as float, required field"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="A store_id is required for each item"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"message": "Item not found"}, 404


    def post(self, name):        
        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists"}, 400

        request_data = Item.parser.parse_args()
        item = ItemModel(name, **request_data)

        try:
            item.save_to_db()
        except:
            return {"message": f"Error in inserting item {item}"}, 500

        return item.json(), 201


    @jwt_required()
    def delete(self, name):

        item = ItemModel.find_by_name(name)

        if item is None:
          return {"message": "Item is not in database"}, 400
        else:
            print('Found item in db, ready to delete')
            try:
                item.delete_from_db()
            except:
                return {"message": f"Error in deleting item {item.json()}"}, 500            

        return {'message': 'item deleted'}, 200


    def put(self, name):
        request_data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **request_data)
        else:
            item.price = request_data["price"]
            item.store_id = request_data["store_id"]

        try:
            item.save_to_db()
        except:
            return {"message": f"Error in inserting item {item.json()}"}, 500

        return item.json(), 201


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}

