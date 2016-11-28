import json
import requests

from bottle import Bottle, request, template, response

import private_variables
import services

app = Bottle()

client_id = private_variables.client_id
client_secret = private_variables.client_secret


@app.route('/', method='GET')
def webshop():
    return template('./static/html/webshop.html')


@app.route('/donate', method='GET')
def get_donate():
    code = request.GET.get('code')
    target = request.GET.get('target')
    target_account_id = target.split('_')[0]
    target_country = target.split('_')[1]
    target_currency = target.split('_')[2]

    target_account_number = target.split('_')[3]
    target_sort_code = target.split('_')[4]
    target_first_name = target.split('_')[5]
    target_last_name = target.split('_')[6]

    def auth(code):
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'code': code,
            'redirect_uri': 'http://localhost:8000/donate?target={target_acc_id}_{target_country}_{target_currency}_'
                            '{target_acc_number}_{target_sort_code}_{target_first_name}_{target_last_name}'.format(
                target_acc_id=target_account_id, target_country=target_country, target_currency=target_currency,
                target_acc_number=target_account_number, target_sort_code=target_sort_code,
                target_first_name=target_first_name, target_last_name=target_last_name)
        }
        resp = requests.post('https://test-restgw.transferwise.com/oauth/token',
                             data=data,
                             auth=(client_id, client_secret))
        return json.loads(resp.text).get('access_token')

    access_token = auth(code)

    def get_profileid(access_token):
        resp = requests.get("https://test-restgw.transferwise.com/v1/profiles",
                            headers=services.get_auth_headers(access_token))

        for p in json.loads(resp.text):
            if p['type'] == 'personal':
                return p['id']

        print('No profile')
        return None

    profile_id = get_profileid(access_token)

    response.set_cookie('profile_id', str(profile_id))
    response.set_cookie('access_token', access_token)
    response.set_cookie('target_account_id', str(target_account_id))
    response.set_cookie('target_country', target_country)
    response.set_cookie('target_currency', target_currency)
    response.set_cookie('target_account_number', str(target_account_number))
    response.set_cookie('target_sort_code', str(target_sort_code))
    response.set_cookie('target_first_name', target_first_name)
    response.set_cookie('target_last_name', target_last_name)

    def get_accounts(access_token, profile_id, target_currency):
        resp = requests.get(
            "https://test-restgw.transferwise.com/v1/accounts?profile={profile_id}".format(profile_id=profile_id),
            headers=services.get_auth_headers(access_token))

        accounts = []
        for a in json.loads(resp.text):
            if not a.get('currency') == target_currency:
                accounts.append({'currency': a.get('currency'),
                                 'accountNumber': a.get('details').get('accountNumber'),
                                 'account_id': a.get('id')})
        return accounts

    source_accounts = get_accounts(access_token, profile_id, target_currency)

    return template('./static/html/donate.html', source_accounts=source_accounts)


@app.route('/submit_donation', method='POST')
def process_donation():
    target_country = request.cookies.get('target_country')
    target_currency = request.cookies.get('target_currency')

    target_account_number = request.cookies.get('target_account_number')
    target_sort_code = request.cookies.get('target_sort_code')
    target_first_name = request.cookies.get('target_first_name')
    target_last_name = request.cookies.get('target_last_name')

    access_token = request.cookies.get('access_token')
    profile_id = request.cookies.get('profile_id')

    source_account = request.forms.get('accounts').split('-')[0]
    source_currency = request.forms.get('accounts').split('-')[1]
    source_amount = request.forms.get('amount')
    message = request.forms.get('message')

    def create_quote(access_token, profileid, sourceCurrency, sourceAmount, targetCurrency):
        payload = {"profile": str(profileid), "rateType": "FIXED",
                   "source": sourceCurrency, "sourceAmount": str(sourceAmount), "target": targetCurrency}

        resp = requests.post("https://test-restgw.transferwise.com/v1/quotes", data=json.dumps(payload),
                             headers=services.get_auth_headers(access_token))
        return json.loads(resp.text).get('id')

    quote_id = create_quote(access_token, profile_id, source_currency, source_amount, target_currency)

    def create_recipient_account(access_token, target_first_name, target_last_name, target_country, target_currency,
                                 target_account_number, target_sort_code):
        payload = {"accountHolderName": target_first_name + " " + target_last_name, "business": "null",
                   "country": target_country, "currency": target_currency, "type": "sort_code",
                   "details": {"legalType": "PRIVATE", "accountNumber": target_account_number,
                               "sortCode": target_sort_code}}

        resp = requests.post("https://test-restgw.transferwise.com/v1/accounts", data=json.dumps(payload),
                             headers=services.get_auth_headers(access_token))
        return json.loads(resp.text).get('id')

    target_recipient_id = create_recipient_account(access_token, target_first_name, target_last_name, target_country,
                                                   target_currency, target_account_number, target_sort_code)

    def create_transfer(access_token, source_account, target_account, quote_id, message):
        payload = {"source_account": source_account, "targetAccount": target_account, "quote": str(quote_id),
                   "reference": message, "payInMethod": "transfer"}

        resp = requests.post("https://test-restgw.transferwise.com/v1/transfers", data=json.dumps(payload),
                             headers=services.get_auth_headers(access_token))
        return json.loads(resp.text)

    final_transaction = create_transfer(access_token, source_account, target_recipient_id, quote_id, message)
    print(final_transaction)

    return template('./static/html/success.html', transaction=final_transaction)
