from flask import current_app as app


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'
