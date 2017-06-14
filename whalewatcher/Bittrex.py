import hashlib, hmac, string, base64
import time
from urllib.request import urlopen, Request
import urllib.parse
import json, urllib

class SignedAPICall(object):
    def __init__(self, api_url, apikey=None, secret=None):
        self.api_url = api_url
        self.apikey = apikey
        self.secret = secret

    def request(self, args):
        self.params = []
        self._sort_request(args)
        self._build_post_request(args)

    def _sort_request(self, args):
        '''creates url friendly string. skips the command and method keys, appends empty keys without a value'''
        keys = sorted(args.keys())
        for key in keys:
            if key in ['command', 'method']:
                pass
            elif args[key] == '':
                self.params.append(key)
            else:
                self.params.append(key + '=' + urllib.parse.quote(str(args[key])))

    def _build_post_request(self, args):
        self.query = '&'.join(self.params)
        if self.apikey:
            self.query += '&apikey=' + urllib.parse.quote(self.apikey)
        self.query += '&nonce=' + urllib.parse.quote(str(int(time.time() * 1000)))
        self.value = self.api_url + args['method'] + '/' + args['command'] + '?' + self.query
        self.headers = {'Content-Type': 'application/json'}
        if self.secret:
            self.headers['apisign']=hmac.new(self.secret.encode(), self.value.encode(), hashlib.sha512).hexdigest()

class Bittrex(SignedAPICall):
    def __getattr__(self, name):
        def handlerFunction(*args, **kwargs):
            if kwargs:
                return self._make_request(name, kwargs)
            return self._make_request(name, args[0])
        return handlerFunction

    def _http_get(self, url):
        req = Request(url)
        for h in self.headers:
            req.add_header(h, self.headers[h])
        response = urlopen(Request(url, headers=self.headers))
        return response.read().decode('utf-8')

    def _make_request(self, command, args):
        args['command'] = command
        self.request(args)
        data = self._http_get(self.value)
        # The response is of the format {commandresponse: actual-data}
        return json.loads(data)


api_url='https://bittrex.com/api/v1.1/'
apikey=''
secret=''

# https://bittrex.com/home/api
request = {'method': 'public' }
if request['method'] == 'public':
    api = Bittrex(api_url)
    request['market']='usdt-eth'
    ticker = api.getticker(request) #withdrawalhistory(request)
    print(json.dumps(ticker, indent=4))
    request['market']='btc-eth'
    btcethsummary = api.getmarketsummary(request)
    request['type']='both'
    request['depth']=20
    print(json.dumps(btcethsummary, indent=4))
    btcethorderbook = api.getorderbook(request)
    print(json.dumps(btcethorderbook, indent=4))
    print(request)
