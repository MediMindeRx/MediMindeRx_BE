from flask import Blueprint
from flask_restful import Api
from resources.Reminder import ReminderResource
from resources.User import UserResource
from resources.Location import LocationResource
from resources.Scheduled import ScheduledResource
from resources.UserId import UserIdResource
from resources.UsersReminder import UsersReminderResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(ReminderResource, '/reminders')
api.add_resource(UserResource, '/users')
api.add_resource(LocationResource, '/locations')
api.add_resource(ScheduledResource, '/scheduled')
api.add_resource(UserIdResource, '/users/<int:id>')
api.add_resource(UsersReminderResource, '/users/<int:user_id>/reminders')
