from flask_restful import Resource
from Model import User, Reminder, ReminderSchema

reminder_schema = ReminderSchema(many=True)


class UsersReminderResource(Resource):
    def get(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'User does not exist'}, 400

        reminders = Reminder.query.filter_by(user_id=user_id)
        reminders = reminder_schema.dump(reminders)
        return reminders, 200
