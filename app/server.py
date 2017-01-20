from bottle import run

from demo import app as demo_app
from generate_button import app as generate_button_app
from static_files import app as static_files_app

demo_app.merge(static_files_app)
demo_app.merge(generate_button_app)
run(demo_app, host='127.0.0.1', port=8000, reloader=True)
