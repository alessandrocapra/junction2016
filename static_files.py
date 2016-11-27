from bottle import Bottle, request, response, static_file

app = Bottle()


@app.route('/css/<filename:re:.*\.css>')
def send_css(filename):
    return static_file(filename, root='static/css', mimetype='text/css')


@app.route('/img/<filename:re:.*\.jpg>')
def send_jpg(filename):
    return static_file(filename, root='static/img', mimetype='img/jpg')


@app.route('/img/<filename:re:.*\.png>')
def send_png(filename):
    return static_file(filename, root='static/img', mimetype='img/png')


@app.route('/fonts/<filename:re:.*\.woff>')
def send_woff(filename):
    return static_file(filename, root='static/fonts')


@app.route('/fonts/<filename:re:.*\.woff2>')
def send_woff2(filename):
    return static_file(filename, root='static/fonts')


@app.route('/fonts/<filename:re:.*\.ttf>')
def send_ttf(filename):
    return static_file(filename, root='static/fonts')


@app.route('/fonts/<filename:re:.*\.eot>')
def send_eot(filename):
    return static_file(filename, root='static/fonts')


@app.route('/getButton', method='GET')
def buttonize():
    return "It works!"


@app.route('/video/<filename:re:.*\.mp4>')
def send_png(filename):
    return static_file(filename, root='static/video', mimetype='video/mp4')
