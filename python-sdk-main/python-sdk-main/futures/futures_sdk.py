# coding:utf-8
import hashlib
import hmac
import json
import time

import requests

acc = {
    'apikey': '',
    'secretkey': ''
}

rest_url = 'https://futures-open-api.bibk8suat.com'
s = requests.Session()


class BIBrest():
    def __init__(self, api_key=acc['apikey'], secret_key=acc['secretkey']):

        self.rest_url = rest_url
        self.__api_key = api_key
        self.__secret_key = secret_key

    def send_req(self, act, path, params, issign=False):
        global headers
        url = rest_url + path
        if not issign:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = requests.request(act, url, params=params, headers=headers).json()
        if issign:
            sign = self.bib_sign(path, act, params)
            if act == 'GET':
                headers = {
                    'X-CH-APIKEY': self.__api_key,
                    'X-CH-TS': self.time_sign,
                    'X-CH-SIGN': sign,
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                string2 = ''
                for key in sorted(params.keys()):
                    string2 += key + '=' + str(params[key]) + '&'
                string2 = string2[:-1]
                url = url + '?' + string2
            elif act == 'POST':
                headers = {
                    'X-CH-APIKEY': self.__api_key,
                    'X-CH-TS': self.time_sign,
                    'X-CH-SIGN': sign,
                    'Content-Type': 'application/json'
                }
            data = s.request(act, url, data=json.dumps(params), headers=headers).json()
        return data

    def get_depth(self, symbol='E-BTC-USDT'):
        url = '/fapi/v1/depth?contractName=%s' % symbol
        data = self.send_req('GET', url, {})
        return data

    def get_ticker(self, symbol='E-BTC-USDT'):
        url = '/fapi/v1/ticker?contractName=%s' % symbol
        data = self.send_req('GET', url, {})
        return data

    def get_coin_base_info(self, symbol_op):
        # symbol_op = ['E-BTC-USDT','E-ETH-USDT']
        url = '/fapi/v1/contracts'
        data = self.send_req('GET', url, {})
        scale = {}
        for i in data:
            if i['symbol'] in symbol_op:
                name = i['symbol']
                scale[name] = {}
                scale[name]['pricedigit'] = i['pricePrecision']
                scale[name]['multiplier'] = i['multiplier']
        return scale

    def get_balance(self):
        url = '/fapi/v1/account'
        # params = {}
        data = self.send_req('GET', url, {}, issign=True)
        return data

    def get_position(self, contractName='E-BTC-USDT'):
        url = '/fapi/v1/positions'
        params = {'contractName': contractName}
        data = self.send_req('GET', url, params, issign=True)
        return data

    def batch_create_order(self, params):
        url = '/fapi/v1/batchRobot'
        # params = {
        #     'contractName':symbol,
        #     'orders':[{
        #         'clientOrderId':'ylkj',
        #         'contractName':symbol,
        #         'open':open,
        #         'positionType':positionType,
        #         'price':price,
        #         'side':side,
        #         'timeInForce':timeInForce,
        #         'volume':volume,
        #         }],
        #     }
        data = self.send_req('POST', url, params, issign=True)
        return data

    def batch_cancel_order(self, params):
        url = '/fapi/v1/batchRobot'
        # params = {
        #     'contractName':contractName,
        #     'orderIds':[1758261800112246834
        #     ],
        #     }
        data = self.send_req('POST', url, params, issign=True)
        return data

    def open_order(self, contractName='E-BTC-USDT'):
        url = '/fapi/v1/openOrders'
        params = {
            'contractName': contractName,
        }
        data = self.send_req('GET', url, params, issign=True)
        return data

    def self_trade(self, params):
        url = '/fapi/v1/selfTrade'
        # params = {
        #     'contractName':contractName,
        #     'price':price,
        #     'volume':volume,
        #     }
        data = self.send_req('POST', url, params, issign=True)
        return data

    def bib_sign(self, path, act, params):
        self.time_sign = str(int((time.time()) * 1000))
        params1 = {
            'time_millies': self.time_sign,
            'method': act,
            'path': path,
        }
        if act == 'GET':
            if params == {}:
                string = params1['time_millies'] + params1['method'] + params1['path']
            else:
                string1 = ''
                for key in sorted(params.keys()):
                    string1 += key + '=' + str(params[key]) + '&'
                string1 = string1[:-1]
                string = params1['time_millies'] + params1['method'] + params1['path'] + '?' + string1
            sign = string
            self.string = string
        elif act == 'POST':
            string = params1['time_millies'] + params1['method'] + params1['path'] + json.dumps(params)
            self.string = string
        m = hmac.new(self.__secret_key.encode("utf-8"), string.encode("utf-8"), hashlib.sha256)
        sign = m.hexdigest()
        self.sign = sign
        return sign

    @staticmethod
    def hello():
        print("hello bib sdk")


if __name__ == '__main__':
    api_key = ''
    secret_key = ''
    client = BIBrest(api_key, secret_key)
    data = client.get_ticker('E-BTC-USDT')
    print(data)
