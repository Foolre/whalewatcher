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

def btrequest(url):
    time.sleep(1)
    uri='https://bittrex.com/api/v1.1{0}'
    headers = { 'Content-Type': 'application/json' }
    headers['apisign'] = hmac.new(secret.encode(), uri.format(url).encode(), hashlib.sha512).hexdigest() 
    #print("requesting {0}".format(uri.format(url)))
    req = Request(uri.format(url), headers=headers)
    response = urlopen(req).read().decode()
    parsed = json.loads(response)
    return parsed["result"]

def comparebidpaid(bid, paid):
    result=((bid - paid ) / ((bid + paid) / 2)) * 100
    if result > float(0):
        return True
    else:
        return False

while True:
    nonce = '&nonce='+urllib.parse.quote(str(int(time.time() * 1000))) + '&apikey=' + apikey
    uri = '/account/getbalance?currency={0}' + nonce
    balance = {}
    balance['btc'] = btrequest(uri.format('btc'))
    balance['eth'] = btrequest(uri.format('eth'))
    uri = '/public/getmarketsummary?market=BTC-ETH'
    market = btrequest(uri)
    uri = '/account/getorderhistory?market=BTC-ETH' + nonce
    history = btrequest(uri)
    print(history)
    exit(1)
    if history['OrderType'] == "LIMIT_BUY":
        unitpricepaid = history["PricePerUnit"]
        amountsell = history["Price"]
        amountbuy = history["Quantity"]
        available = balance['eth']['Available']
        unitbid = market[0]['Bid']
        difference = float((amountbuy * unitbid ) - amountsell)
        if comparebidpaid(unitbid, unitpricepaid):
            print('profit: btc {0:f}'.format(difference))
        else:
            loss = float((amountbuy * unitbid ) - amountsell)
            print('loss btc {0:f}'.format(difference))
    time.sleep(5)
