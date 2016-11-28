import qrcode

from bottle import request, template, response, Bottle
from io import BytesIO

app = Bottle()


@app.route('/register', method='GET')
def create():
    code = request.GET.get('code')
    return template('./static/html/registerButton.html')


@app.route('/qr', method='GET')
def get_image():
    img = qrcode.make(request.query['url'])

    with BytesIO() as output:
        img.save(output, 'PNG')
        data = output.getvalue()

    response.set_header('Content-type', 'image/png')
    return data
