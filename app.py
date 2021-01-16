from auth import auth as auth_blueprint
from models import User, EventModel
from flask import Flask
from db import db
from flask_login import LoginManager
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin
# from flask_statistics import Statistics

# Google Calendar imports
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import timedelta, datetime
import pickle, os.path
############################################
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:mysql@localhost/doctoradmin4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'testxyz'
# app.config['STATISTICS_DEFAULT_DATE_SPAN'] = True
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

db_adapter = SQLAlchemyAdapter(db,  User)
user_manager = UserManager(db_adapter, app)

# statistics = Statistics(app, db, Request)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


# blueprint for auth routes in our app
app.register_blueprint(auth_blueprint)


############################################

@app.before_first_request
def create_table():
    database = "doctoradmin4"

    engine = db.create_engine(
        "mysql+mysqlconnector://root:mysql@localhost", {}
    )  # connect to server
    existing_databases = engine.execute("SHOW DATABASES")
    existing_databases = [d[0] for d in existing_databases]

    if database not in existing_databases:
        engine.execute("CREATE DATABASE iF NOT EXISTS {}".format(database))

    db.create_all()


# def main(start_time):
#     SCOPES = ["https://www.googleapis.com/auth/calendar"]
#     creds = None

#     if os.path.exists("token.pickle"):
#         with open("token.pickle", "rb") as token:
#             creds = pickle.load(token)

#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "date_perm.json", SCOPES
#             )
#             creds = flow.run_local_server(port=0)
#         with open("token.pickle", "wb") as token:
#             pickle.dump(creds, token)

#     service = build("calendar", "v3", credentials=creds)

#     app_date = start_time.strftime("%Y/%m/%d")

#     y1, m1, d1 = [int(x) for x in app_date.split("/")]

#     app_date = datetime(y1, m1, d1, 9, 0, 0)

#     end_time = app_date + timedelta(hours=4)
#     event = {
#         "summary": "Doctor Appointment",
#         "location": "Cairo",
#         "description": "",
#         "start": {
#             "dateTime": app_date.strftime("%Y-%m-%dT%H:%M:%S"),
#             "timeZone": "Africa/Cairo",
#         },
#         "end": {
#             "dateTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
#             "timeZone": "Africa/Cairo",
#         },

#     },
#     service.events().insert(calendarId="primary", body=event).execute()
#     new_event = EventModel()
    
    
    
if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
