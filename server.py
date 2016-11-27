from bottle import run

from endpoints import app as endpoints_app
from static_files import app as static_files_app

endpoints_app.merge(static_files_app)
run(endpoints_app, host='127.0.0.1', port=8000, reloader=True)
