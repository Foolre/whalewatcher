#!/usr/bin/python3
import hmac, hashlib
import json
import urllib
from urllib.request import urlopen, Request
import time

import credentials
from credentials import apikey, secret
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

def btrequest(uri):
    time.sleep(1)
    url='https://bittrex.com/api/v1.1{0}'
    headers = { 'Content-Type': 'application/json' }
    headers['apisign'] = hmac.new(secret.encode(), url.format(uri).encode(), hashlib.sha512).hexdigest() 
    req = Request(url.format(uri), headers=headers)
    response = urlopen(req).read().decode()
    parsed = json.loads(response)
    return parsed['result']

def comparebidpaid(marketbid, pricepaid):
    result=((marketbid - pricepaid ) / ((marketbid + pricepaid) / 2)) * 100
    if result > float(5):
        return True
    else:
        return False

def nonce(uri):
    '''calculates this nonce thingy and puts together the uri string'''
    result = uri + '&nonce=' + str(int(time.time() * 1000 )) + '&apikey=' + apikey
    return result

uri = nonce('/account/getbalance?currency={0}')
balance = {'btc': btrequest(uri.format('btc')),
           'eth': btrequest(uri.format('eth'))
          }

uri = nonce('/account/getorderhistory?market={0}')
history = btrequest(uri.format('btc-eth'))
lastpurchase = history[0]
if lastpurchase['OrderType'] == 'LIMIT_BUY':
    #bought eth paid with btc
    ethquantity = lastpurchase['Quantity'] - lastpurchase['Commission']
    btcquantity = lastpurchase['Price']
    pricepaid = float(btcquantity / ethquantity)

uri = '/public/getmarketsummary?market={0}'
sell = '/market/selllimit?market={0}&quantity={1}&rate={2}'
while True:
    market = btrequest(uri.format('btc-eth'))
    marketbid = market[0]['Bid']
    difference = marketbid - pricepaid
    if comparebidpaid(marketbid, pricepaid):
        order = sell.format('btc-eth', ethquantity, marketbid)
        print('profit: btc {0:f}'.format(difference))
        exit(1)
    else:
        print('loss btc {0:f}'.format(difference))
    time.sleep(5)
