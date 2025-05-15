from flask import Flask
from Backend.models import db
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.sqlite3"
    app.config["SECRET_KEY"] = "mysecretkey"
    db.init_app(app)
    login_mnger = LoginManager( app)
    @login_mnger.user_loader
    def load_user(email):
        user = db.session.query(User).filter_by(email = email).first() or \
              db.session.query(Admin).filter_by(email = email).first() or \
                  db.session.query(Professional).filter_by(email = email).first()
        return user

    app.app_context().push()
    return app

app = create_app()

from Backend.routes import *
from Backend.create_data import *

if __name__ == "__main__":
    app.run(debug=True)