from auth import auth as auth_blueprint
from models import User
from flask import Flask
from db import db
from flask_login import LoginManager
from flask_user import SQLAlchemyAdapter, UserManager

############################################
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:mysql@localhost/EmergencyT04"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'Emergency'

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

db_adapter = SQLAlchemyAdapter(db,  User)
user_manager = UserManager(db_adapter, app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


# blueprint for auth routes in our app
app.register_blueprint(auth_blueprint)


############################################

@app.before_first_request
def create_table():
    database = "EmergencyT04"

    engine = db.create_engine(
        "mysql+mysqlconnector://root:mysql@localhost", {}
    )  # connect to server
    existing_databases = engine.execute("SHOW DATABASES")
    existing_databases = [d[0] for d in existing_databases]

    if database not in existing_databases:
        engine.execute("CREATE DATABASE iF NOT EXISTS {}".format(database))

    db.create_all()


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True)
