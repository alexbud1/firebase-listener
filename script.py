import firebase_admin
from firebase_admin import db
import os
from os.path import join, dirname
from dotenv import load_dotenv

##### .env adjustments
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


cred_obj = firebase_admin.credentials.Certificate(os.environ.get("SECRET_FILE"))
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':os.environ.get("DATABASE_URL")
	})
ref = db.reference('/Requests')


def ignore_first_call(fn):
    called = False

    def wrapper(*args, **kwargs):
        nonlocal called
        if called:
            return fn(*args, **kwargs)
        else:
            called = True
            return None

    return wrapper


@ignore_first_call
def listener(event):
    print(event.event_type)  # can be 'put' or 'patch'
    print(event.path)  # relative to the reference, it seems
    print(event.data)  # new data at /reference/event.path. None if deleted

    ##### call script here


db.reference('/Requests').listen(listener)