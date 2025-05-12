from flask import current_app as app


@app.route("/")
def index():
    return "Hello world"


@app.route("/welcome")
def welcome():
    return "welcome user"