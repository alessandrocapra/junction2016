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
   return template('index.html', access_token='', targetAccount='', sourceAccounts='')


@app.route('/webshop', method='GET')
def create():
   code = request.GET.get('code')
   return template('webshop.html')

@app.route('/donate', method='GET')
def get_donate():
   code = request.GET.get('code')
   targetAccountId = request.GET.get('targetAccount')
   print(code)
   data = {
      'grant_type': 'authorization_code',
      'client_id': 'f272f4a3-ecc1-44fe-b3f4-9a20e9433f4e',
      'code': code,
      'redirect_uri': 'http://localhost:8000/donate?targetAccount=' + targetAccountId
   }
   resp = requests.post('https://test-restgw.transferwise.com/oauth/token',
      data=data, auth=('f272f4a3-ecc1-44fe-b3f4-9a20e9433f4e', '534cda42-719c-4b26-86c2-c96b7cb03437'))
   access_token = json.loads(resp.text).get('access_token')

   

   def get_profileid(access_token):
      headers = {
         'accept': "application/json",
         'authorization': "Bearer " + access_token
      }

      respProfiles = requests.get("https://test-restgw.transferwise.com/v1/profiles", headers=headers)

      for p in json.loads(respProfiles.text):
         if p['type'] == 'personal':
            return p['id']
      
      print ('No profile')
      return None





   def get_accounts(access_token, profileid):

      headers = {
         'accept': "application/json",
         'authorization': "Bearer " + access_token 
      }

      respAccounts = requests.get("https://test-restgw.transferwise.com/v1/accounts?profile=" + str(profileid), headers=headers)
      
      accounts = []
      for a in json.loads(respAccounts.text):
         accounts.append({'currency': a.get('currency'),
                        'accountNumber': a.get('details').get('accountNumber')})
      return accounts

   profileid = get_profileid(access_token)

   sourceAccounts = get_accounts(access_token, profileid)

   print(sourceAccounts)

   # selected from form
   sourceAccount = sourceAccounts[0].get('accountNumber')
   sourceCurrency = sourceAccounts[0].get('currency')

   print('sourceAccount', sourceAccount)
   print('sourceCurrency', sourceCurrency)

   sourceAmount = 100


   headers = {
         'accept': "application/json",
         'authorization': "Bearer " + access_token 
      }

   resp = requests.get("https://test-restgw.transferwise.com/v1/accounts/" + str(targetAccountId), headers=headers)


   target_account = json.loads(resp.text)
   targetCurrency = target_account.get('currency')
   print('targetCurrency', targetCurrency)

   message = 'Test sjssj'
   
   
   return template('index.html', access_token=access_token, targetAccount=targetAccountId, sourceAccounts=sourceAccounts)


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
