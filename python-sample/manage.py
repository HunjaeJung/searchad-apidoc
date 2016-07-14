#-*- encoding: utf-8 -*-
import time
import hmac
import hashlib
import base64
import requests
import json
from naver_api_config import BASE_URL, API_KEY, SECRET_KEY, CUSTOMER_ID

def generate_signature(timestamp, method, api_path, secret_key):
    s = '{0}.{1}.{2}'.format(timestamp, method, api_path)
    return base64.b64encode(hmac.new(secret_key, msg=s, digestmod=hashlib.sha256).digest())


def get_header(method, api_path):
    timestamp = int(time.time())
    return {
        'X-Customer' : CUSTOMER_ID,
        'X-API-KEY'  : API_KEY,
        'X-Timestamp': timestamp,
        'X-Signature': generate_signature(timestamp, method, api_path, SECRET_KEY)
    }


def pretty_print(data):
    print json.dumps(data, sort_keys=True, indent=4, separators=(',',': '))


class APIRequest():
    def __init__(self, method, api_path_with_params):
        self.method = method
        self.api_path = api_path_with_params.split('?')[0]
        self.endpoint = BASE_URL+api_path_with_params

    def call(self, data=None):
        if self.method == 'GET':
            res = requests.get(self.endpoint, headers=get_header('GET', self.api_path))

        elif self.method == 'POST':
            if data is not None and type(data) is not str:
                data = json.dumps(data)
            res = requests.post(self.endpoint, data=data, headers=get_header('POST', self.api_path))

        elif self.method == 'DELETE':
            res = requests.delete(self.endpoint, headers=get_header('DELETE', self.api_path))

        elif self.method == 'PUT':
            res = requests.put(self.endpoint, data=data, headers=get_header('PUT', self.api_path))

        else:
            raise Exception('Method not allowed')

        res = eval(res.text.replace('false', 'False').replace('true','True'))
        pretty_print(res)

        return res


# Sanity Check
res = APIRequest('POST', '/estimate/performance-bulk').call({
  "items":[
    {
      "keyword":"제주여행",
      "bid":70,
      "device":"PC",
      "keywordplus":False
    },
    {
      "keyword":"제주도",
      "bid":70,
      "device":"PC",
      "keywordplus":False
    },
    {
      "keyword":"맛집",
      "bid":70,
      "device":"PC",
      "keywordplus":False
    },
    {
      "keyword":"여행",
      "bid":70,
      "device":"PC",
      "keywordplus":False
    }
  ]
})
print res
