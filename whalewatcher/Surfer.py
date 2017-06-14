#!/usr/bin/python3
import json
import urllib
from urllib.request import urlopen, Request
import time

try:
    import credentials.py
except:
    apikey=''
    secret=''
    api_url='https://bittrex.com/api/v1.1/'

PUBLIC_COMMANDS = '''{
    "getmarkets": null,
    "getcurrencies": null,
    "getticker": null,
    "getmarketsummaries": "market",
    "getorderbook": [ "market","type","depth" ],
    "getmarkethistory": "market"
}'''

MARKET_COMMANDS = '''{
    "buylimit": [ "market", "quantity", "rate" ],
    "sellimit": [ "market", "quantity", "rate" ],
    "cancel": [ "market", "quantity", "rate" ] ,
    "getopenorders": [ "market" ]
}'''

ACCOUNT_COMMANDS = '''{
    "getbalances": null,
    "getbalance": "currency",
    "getdepositaddress": "currency",
    "withdraw": [ "currency", "quantity", "address", "paymentid" ]
    "getorder": "uuid",
    "getorderhistory": "market",
    "getwithdrawalhistory": "currency",
    "getdeposithistory": "currency"
}'''

def request(*args, **kwargs):
    uri='https://bittrex.com/api/v1.1/'
    if args[0] == 'public':
        url=uri+args[0]+'/'+args[1]+'?'

    headers = kwargs['headers']
    del kwargs['headers']
    quote_url_string(kwargs)
    build_request(url)

def quote_url_string(kwargs):
    keys = sorted(kwargs.keys())
    for key in keys:
        params.append(key + '=' + urllib.parse.quote(str(kwargs[key])))

def build_request(url):
    query = url + '&'.join(params)
    print(query)
    exit(1)
    req = urlopen(Request(url + query, headers=headers))
    print(req.read())

params = []
headers = { 'Content-Type': 'application/json' }
nonce = urllib.parse.quote(str(int(time.time() * 1000)))
markets = 'BTC-ETH'
request('public','getorderbook', headers=headers, nonce=nonce, markets=markets)
#url = 'https://bittrex.com/api/v1.1/public/getorderbook?'

#headers['apisign']=hmac.new(secret.encode(), url.encode(), hashlibe.sha512).hexdigest()

#test=BittrexSurfer()
#print(test)
