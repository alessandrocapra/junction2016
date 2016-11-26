from bottle import Bottle, run, request, template, response, HTTPResponse, static_file
import requests
import json
import qrcode
from PIL import Image
from io import BytesIO
import pprint

app = Bottle()

@app.route('/', method='GET')
def homepage():
   return template('index.html', access_token='', targetAccount='')


@app.route('/webshop', method='GET')
def create():
   code = request.GET.get('code')
   return template('webshop.html')

@app.route('/donate', method='GET')
def get_donate():
   code = request.GET.get('code')
   targetAccount = request.GET.get('targetAccount')
   print(code)
   data = {
      'grant_type': 'authorization_code',
      'client_id': 'f272f4a3-ecc1-44fe-b3f4-9a20e9433f4e',
      'code': code,
      'redirect_uri': 'http://localhost:8000/donate?targetAccount=' + targetAccount
   }
   respToken = requests.post('https://test-restgw.transferwise.com/oauth/token',
      data=data, auth=('f272f4a3-ecc1-44fe-b3f4-9a20e9433f4e', '534cda42-719c-4b26-86c2-c96b7cb03437'))
   

   def get_profileid(respToken):
      headers = {
         'accept': "application/json",
         'authorization': "Bearer " + respToken
      }

      respProfiles = requests.get("https://test-restgw.transferwise.com/v1/profiles", headers=headers)

      for p in json.loads(respProfiles.text):
         if p['type'] == 'personal':
            return p['id']
      
      print ('No profile')
      return None





   def get_accounts(respToken):
      profileid = get_profileid(respToken)
      headers = {
         'accept': "application/json",
         'authorization': "Bearer " + respToken 
      }

      respAccounts = request.get("https://test-restgw.transferwise.com/v1/accounts?profile="+profileid, headers=headers)
      
      for a in json.loads(respAccounts.text):
         pprint.pprint(a);

   get_accounts(respToken)
   #getAccounts 
   sourceAccounts = []

   sourceAccount = ''
   sourceCurrency = ''
   sourceAmount = 0

   targetCurrency = ''

   message = ''
   
   
   return template('index.html', access_token=json.loads(resp.text).get('access_token'), targetAccount=targetAccount)


@app.route('/css/<filename:re:.*\.css>')
def send_css(filename):
   print(filename)
   return static_file(filename, root='static/css', mimetype='text/css')

@app.route('/img/<filename:re:.*\.jpg>')
def send_jpg(filename):
   return static_file(filename, root='static/img', mimetype='img/jpg')

@app.route('/img/<filename:re:.*\.png>')
def send_png(filename):
   return static_file(filename, root='static/img', mimetype='img/png')


@app.route('/getButton', method='GET')
def buttonize():
    return "It works!"

@app.route('/qr', method='GET')
def get_image():

   img = qrcode.make(request.query['url'])

   with BytesIO() as output:
      img.save(output, 'PNG')
      data = output.getvalue()

   response.set_header('Content-type', 'image/png')

   return data


@app.route('/register', method='GET')
def create():
   code = request.GET.get('code')
   return template('registerButton.html')

run(app, host='127.0.0.1', port=8000)
