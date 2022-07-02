import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token
from models.user import UserModel
        
class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="Username, required field"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="Password, required field"
    )

    def post(self):

        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": f"A user with name = {data['username']} already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully!"}, 201


class Login(Resource):

    def post(self):
        print('in post method')
        parser = reqparse.RequestParser()
        parser.add_argument('username',
            required=True,
            help="String for username, required field"
        )
        parser.add_argument('password',
            required=True,
            help="String for password, required field"
        )
        request_data = parser.parse_args()

        username = request_data["username"]
        password = request_data["password"]
        if username is None or password is None:
            return {"msg": "Bad username or password"}, 401

        access_token = create_access_token(identity=username)
        return {"access_token": access_token}, 201 