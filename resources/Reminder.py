from flask import request
from flask_restful import Resource
from Model import db, Reminder, ReminderSchema

reminders_schema = ReminderSchema(many=True)
reminder_schema = ReminderSchema()


class ReminderResource(Resource):
    def get(self):
        reminders = Reminder.query.all()
        reminders = reminders_schema.dump(reminders)
        return reminders, 200

    def post(self):
        json_data = request.get_json(force=True)
        reminder = Reminder.query.filter_by(title=json_data['title']).first()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        if reminder:
            return {'message': 'Reminder already exists'}, 400

        reminder = Reminder(
            title=json_data['title'],
            user_id=json_data['user_id'],
            supplies=json_data['supplies'],
            show_supplies=json_data['show_supplies'])

        db.session.add(reminder)
        db.session.commit()
        result = reminder_schema.dump(reminder)
        return result, 201

    def put(self):
        json_data = request.get_json(force=True)
        reminder = Reminder.query.filter_by(id=json_data['id']).first()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        if not reminder:
            return {'message': 'Reminder does not exist'}, 400

        reminder = Reminder.query.filter_by(id=json_data['id']).first()
        reminder.show_supplies = json_data['show_supplies']
        reminder.supplies = json_data['supplies']
        reminder.title = json_data['title']
        db.session.commit()
        result = reminder_schema.dump(reminder)
        return result, 200

    def delete(self):
        json_data = request.get_json(force=True)
        reminder = Reminder.query.filter_by(id=json_data['id']).first()
        if not json_data:
            return {'message': 'No input data provided'}, 400
        elif not reminder:
            return {'message': 'Reminder does not exist'}, 400

        Reminder.query.filter_by(id=json_data['id']).delete()
        db.session.commit()
        return {'message': 'Reminder successfully deleted'}, 200
