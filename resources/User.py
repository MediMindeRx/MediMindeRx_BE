from flask import request
from flask_restful import Resource
from Model import db, User, UserSchema

users_schema = UserSchema(many=True)
user_schema = UserSchema()


class UserResource(Resource):
    def get(self):
        users = User.query.all()
        users = users_schema.dump(users)
        return users, 200

    def post(self):
        json_data = request.get_json(force=True)
        user = User.query.filter_by(name=json_data['name']).first()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        elif user:
            return {'message': 'User already exists'}, 400

        user = User(name=json_data['name'])

        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)
        return result, 201

    def put(self):
        json_data = request.get_json(force=True)
        user = User.query.filter_by(id=json_data['id']).first()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        elif not user:
            return {'message': 'User does not exist'}, 400

        user = User.query.filter_by(id=json_data['id']).first()
        user.name = json_data['name']
        db.session.commit()
        result = user_schema.dump(user)
        return result, 200

    def delete(self):
        json_data = request.get_json(force=True)
        user = User.query.filter_by(id=json_data['id']).first()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        elif not user:
            return {'message': 'User does not exist'}, 400

        User.query.filter_by(id=json_data['id']).delete()
        db.session.commit()
        return {'message': 'User has been successfully deleted'}, 200
