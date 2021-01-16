from db import db
from flask_user import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'allUsersTable'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    national_id = db.Column(db.String(80), unique=True)  #
    department = db.Column(db.String(80))
    nationality = db.Column(db.String(80))  #
    phone_num = db.Column(db.String(80))  #

    # only for admins:
    secret_key = db.Column(db.String(50))

    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))

    active = db.Column('is_active', db.Boolean(),
                       nullable=False, server_default='0')


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'allUsersTable.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'role.id', ondelete='CASCADE'))


class contactForm(db.Model):
    __tablename__ = 'contactmsgs'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    subject = db.Column(db.String(1000))
    message = db.Column(db.String(10000))


class PatientModel(db.Model):

    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(80))
    email = db.Column(db.String(100))
    age = db.Column(db.Integer)
    national_id = db.Column(db.String(80), unique=True)
    medical_history = db.Column(db.String(1000))
    phone_num = db.Column(db.String(80))  # Check
    Address = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    enter = db.Column(db.DateTime)
    leave = db.Column(db.DateTime)

    action = db.Column(db.String(100))
    files = db.relationship('FileModel', lazy='dynamic')


class FileModel(db.Model):

    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))


class EventModel(db.Model):

    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    title = db.Column(db.String(300))
    description = db.Column(db.String(300))

    doctor_id = db.Column(db.Integer, db.ForeignKey('allUsersTable.id'))
