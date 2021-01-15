from db import db
from flask_user import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'allUsersTable'
    id = db.Column(db.Integer, primary_key=True )
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    national_id = db.Column(db.String(80), unique=True)  #
    department = db.Column(db.String(80))
    nationality = db.Column(db.String(80))  #
    phone_num = db.Column(db.String(80))  #
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))

    active = db.Column('is_active', db.Boolean(),
                       nullable=False, server_default='0')


class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True )
    name = db.Column(db.String(50))


class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True )
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'allUsersTable.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey(
        'role.id', ondelete='CASCADE'))




class contactForm(db.Model):
    __tablename__ = 'contactmsgs'
    id = db.Column(db.Integer(), primary_key=True )
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    subject = db.Column(db.String(1000))
    message = db.Column(db.String(10000))




class PatientModel(db.Model):

    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True )

    name = db.Column(db.String(80))
    email = db.Column(db.String(100))
    age = db.Column(db.Integer)
    national_id = db.Column(db.String(80), unique=True)
    medical_history = db.Column(db.String(1000))
    phone_num = db.Column(db.String(80))  # Check
    Address = db.Column(db.String(100))
    gender = db.Column(db.String(10))

    action = db.Column(db.String(100))
    files = db.relationship('FileModel', lazy='dynamic')



class FileModel(db.Model):

    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(300))
    # data = db.Column(db.LargeBinary)

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))


# class Request(db.Model):
#     __tablename__ = "request"

#     index = db.Column(db.Integer, primary_key=True )
#     response_time = db.Column(db.Float)
#     date = db.Column(db.DateTime)
#     method = db.Column(db.String(100))
#     size = db.Column(db.Integer)
#     status_code = db.Column(db.Integer)
#     path = db.Column(db.String)
#     user_agent = db.Column(db.String)
#     remote_address = db.Column(db.String)
#     exception = db.Column(db.String)
#     referrer = db.Column(db.String)
#     browser = db.Column(db.String)
#     platform = db.Column(db.String)
#     mimetype = db.Column(db.String)