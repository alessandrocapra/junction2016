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


@app.route('/create-button', method='GET')
def create():
   code = request.GET.get('code')
   return template('create-button.html')


@app.route('/donate', method='GET')
def get_donate():
   code = request.GET.get('code')
   target = request.GET.get('target')
   targetAccountId = target.split('_')[0]
   targetCountry = target.split('_')[0]
   targetCurrency = target.split('_')[2]
   targetAccountNumber = target.split('_')[3]
   targetSortCode = target.split('_')[4]
   targetFirstName = target.split('_')[5]
   targetLastName = target.split('_')[6]
   
   print(code)
   data = {
      'grant_type': 'authorization_code',
      'client_id': 'f272f4a3-ecc1-44fe-b3f4-9a20e9433f4e',
      'code': code,
      'redirect_uri': 'http://localhost:8000/donate?target=' + targetAccountId + '_' + targetCurrency
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
                        'accountNumber': a.get('details').get('accountNumber'),
                        'account_id': a.get('id')})
      return accounts

   profileid = get_profileid(access_token)

   sourceAccounts = get_accounts(access_token, profileid)

   print(sourceAccounts)

   # selected from form
   sourceAccount = sourceAccounts[3].get('account_id')
   sourceCurrency = sourceAccounts[3].get('currency')

   print('sourceAccount', sourceAccount)
   print('sourceCurrency', sourceCurrency)
   print('targetCurrency', targetCurrency)

   sourceAmount = 100

   message = 'Test sjssj'

   def create_quote(access_token, profileid, sourceCurrency, sourceAmount, targetCurrency):
      payload = "{\"profile\":" + str(profileid) + ",\"rateType\":\"FIXED\", \
                  \"source\":\"" + sourceCurrency + "\",\"sourceAmount\":" + str(sourceAmount) + ",\"target\":\"" + targetCurrency + "\"}"


      headers = {
          'accept': "application/json",
          'authorization': "Bearer " + access_token,
          'content-type': "application/json"
          }

      resp = requests.post("https://test-restgw.transferwise.com/v1/quotes", data=payload, headers=headers)
      return json.loads(resp.text).get('id')

   quote_id = create_quote(access_token, profileid, sourceCurrency, sourceAmount, targetCurrency)

   print('quote_id', quote_id)

   def create_transfer(access_token, source_account, target_account, quote_id, message):
      payload = "{\"sourceAccount\":" + str(source_account) + ",\"targetAccount\":" + target_account + ",\"quote\":" + str(quote_id) + ",\
                  \"reference\":\"Early\",\"payInMethod\":\"transfer\"}"
      print('payload', payload)

      headers = {
          'accept': "application/json",
          'authorization': "Bearer " + access_token,
          'content-type': "application/json"
          }

      import ipdb; ipdb.set_trace();
      resp = requests.post("https://test-restgw.transferwise.com/v1/transfers", data=payload, headers=headers)
      print('sahsah')
      print('ashasj')

   create_transfer(access_token, sourceAccount, targetAccountId, quote_id, message)
   
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

@app.route('/video/<filename:re:.*\.mp4>')
def send_png(filename):
   return static_file(filename, root='static/video', mimetype='video/mp4')

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
