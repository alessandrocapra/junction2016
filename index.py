from bottle import Bottle, run, request, template, response
import requests
import json
#import qrcode
#from PIL import Image


app = Bottle()


@app.route('/', method='GET')
def homepage():

   #img = qrcode.make('TODO add link')
   return template('index.html', code='', access_token='')

@app.route('/webshop', method='GET')
def create():
   code = request.GET.get('code')
   return template('webshop.html')

@app.route('/token', method='GET')
def get_token():
   code = request.GET.get('code')
   print(code)
   data = {
      'grant_type': 'authorization_code',
      'client_id': 'f272f4a3-ecc1-44fe-b3f4-9a20e9433f4e',
      'code': code,
      'redirect_uri': 'http://127.0.0.1:8000/token'
   }
   resp = requests.post('https://test-restgw.transferwise.com/oauth/token',
      data=data, auth=('f272f4a3-ecc1-44fe-b3f4-9a20e9433f4e', '534cda42-719c-4b26-86c2-c96b7cb03437'))
   return template('index.html', access_token=json.loads(resp.text).get('access_token'), code='')

@app.route('/getButton', method='GET')
def buttonize():
    return "It works!"

run(app, host='127.0.0.1', port=8000)
