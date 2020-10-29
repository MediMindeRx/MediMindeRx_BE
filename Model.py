from marshmallow_jsonapi import fields, Schema
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name


class Reminder(db.Model):
    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    supplies = db.Column(db.String(250), nullable=False)
    show_supplies = db.Column(db.Boolean, nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('reminders', lazy='dynamic'))
    scheduled_id = db.Column(db.Integer, db.ForeignKey('scheduleds.id', ondelete='CASCADE'), nullable=True)
    scheduled_reminder = db.relationship('Scheduled', backref=db.backref('reminders', lazy='dynamic'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id', ondelete='CASCADE'), nullable=True)
    location_reminder = db.relationship('Location', backref=db.backref('reminders', lazy='dynamic'))

    def __init__(self, title, user_id, supplies, show_supplies, location_id=None, scheduled_id=None):
        self.title = title
        self.user_id = user_id
        self.supplies = supplies
        self.show_supplies = show_supplies
        self.location_id = location_id
        self.scheduled_id = scheduled_id


class Location(db.Model):
    __tablename__ = 'locations'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    location_name = db.Column(db.String(250), nullable=False)
    longitude = db.Column(db.String(50), nullable=False)
    latitude = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, location_name, longitude, latitude):
        self.location_name = location_name
        self.longitude = longitude
        self.latitude = latitude


class Scheduled(db.Model):
    __tablename__ = 'scheduleds'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    unix_date = db.Column(db.String(250), nullable=False)
    days = db.Column(db.String(50), nullable=False)
    times = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, unix_date, days, times):
        self.unix_date = unix_date
        self.days = days
        self.times = times


class ScheduledSchema(Schema):
    class Meta:
        type_ = 'scheduled'
        strict = True
    id = fields.Integer(dump_only=True)
    unix_date = fields.String(required=True)
    days = fields.String(required=True)
    times = fields.String(required=True)
    creation_date = fields.DateTime()


class LocationSchema(Schema):
    class Meta:
        type_ = 'location'
        strict = True
    id = fields.Integer(dump_only=True)
    location_name = fields.String(required=True)
    longitude = fields.String(required=True)
    latitude = fields.String(required=True)
    creation_date = fields.DateTime()


class UserSchema(Schema):
    class Meta:
        type_ = 'users'
        strict = True
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    creation_date = fields.DateTime()


class ReminderSchema(ma.Schema, Schema):
    class Meta:
        type_ = 'reminders'
        strict = True
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    title = fields.String(required=True)
    supplies = fields.String(required=True)
    show_supplies = fields.Boolean(required=True)
    creation_date = fields.DateTime()
    location_reminder = ma.Nested(LocationSchema)
    scheduled_reminder = ma.Nested(ScheduledSchema)
