from flask_restful import Resource
from Model import db, User, UserSchema

users_schema = UserSchema(many=True)
user_schema = UserSchema()


class UserIdResource(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()
        if not user:
            return {'message': 'User does not exist'}, 400

        user = User.query.filter_by(id=id)
        user = users_schema.dump(user)
        return user, 200
