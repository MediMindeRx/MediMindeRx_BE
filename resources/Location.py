from flask import request
from flask_restful import Resource
from Model import db, Location, LocationSchema, Reminder

locations_schema = LocationSchema(many=True)
location_schema = LocationSchema()


class LocationResource(Resource):
    @staticmethod
    def post():
        json_data = request.get_json(force=True)
        location = Location.query.filter_by(location_name=json_data['location_name']).first()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        elif location:
            return {'message': 'Location reminder already exists'}, 400

        new_location = Location(
            location_name=json_data['location_name'],
            longitude=json_data['longitude'],
            latitude=json_data['latitude'])
        db.session.add(new_location)
        db.session.commit()
        location = db.session.query(Location).order_by(Location.id.desc()).first()

        reminder = Reminder.query.filter_by(id=json_data['reminder_id']).first()
        reminder.location_id = location.id
        db.session.commit()
        result = location_schema.dump(new_location)
        return result, 201
