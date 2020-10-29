from flask import request
from flask_restful import Resource
from Model import db, Scheduled, ScheduledSchema, Reminder

scheduleds_schema = ScheduledSchema(many=True)
scheduled_schema = ScheduledSchema()


class ScheduledResource(Resource):
    def post(self):
        json_data = request.get_json(force=True)

        new_scheduled = Scheduled(unix_date=json_data['unix_date'], days=json_data['days'], times=json_data['times'])
        db.session.add(new_scheduled)
        db.session.commit()
        scheduled = db.session.query(Scheduled).order_by(Scheduled.id.desc()).first()

        reminder = Reminder.query.filter_by(id=json_data['reminder_id']).first()
        reminder.scheduled_id = scheduled.id
        db.session.commit()
        result = scheduled_schema.dump(new_scheduled)
        return result, 201
