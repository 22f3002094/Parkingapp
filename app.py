from flask import Flask
from Backend.models import db

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.sqlite3"
    db.init_app(app)
    
    app.app_context().push()
    return app

app = create_app()

from Backend.routes import *
from Backend.create_data import *

if __name__ == "__main__":
    app.run(debug=True)