# coding:utf-8
import hashlib
import time

import requests

acc = {
    'apikey': '',
    'secretkey': ''
}

resturl = 'https://openapi.bibk8suat.com'
s = requests.Session()


class BIBrest():
    def __init__(self, api_key=acc['apikey'], secret_key=acc['secretkey']):
        self.resturl = resturl
        self.__api_key = api_key
        self.__secret_key = secret_key

    def send_req(self, act, path, params, issign=False):
        url = resturl + path
        if not issign:
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = requests.request(act, url, params=params, headers=headers).json()
        if issign:
            sign = self.bib_sign(path, act, params)
            if act == 'GET':
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                params1 = {
                    'api_key': self.__api_key,
                    'time': self.time_sign,
                    'sign': sign,
                }
                params1.update(params)
                payload = ''
                for key in sorted(params1.keys()):
                    payload += key + '=' + str(params1[key]) + '&'
                payload = payload[:-1]
                url = url + '?' + payload
                payload = {}
            elif act == 'POST':
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                params2 = {
                    'api_key': self.__api_key,
                    'time': self.time_sign,
                    'sign': sign,
                }
                params2.update(params)
                payload = ''
                for key in sorted(params2.keys()):
                    payload += key + '=' + str(params2[key]) + '&'
                payload = payload[:-1]
            data = s.request(act, url, headers=headers, data=payload).json()
        return data

    def get_depth(self, symbol='btcusdt', type='step0'):
        url = '/open/api/market_dept'
        params = {
            'symbol': symbol,
            'type': type,
        }
        data = self.send_req('GET', url, params)
        return data

    def get_ticker(self, symbol='btcusdt'):
        url = '%s' % symbol
        data = self.send_req('GET', url, {})
        return data

    def get_coin_base_info(self, symbol_op):
        # symbol_op = ['btcusdt','ethusdt']
        url = '/open/api/common/symbols'
        data = self.send_req('GET', url, {})
        scale = {}
        for i in data['data']:
            if i['symbol'].lower() in symbol_op:
                name = i['symbol'].lower()
                scale[name] = {}
                scale[name]['pricedigit'] = i['price_precision']
                scale[name]['voldigit'] = i['amount_precision']
        return scale

    def get_balance(self):
        url = '/open/api/user/account'
        # params = {}
        data = self.send_req('POST', url, {}, issign=True)
        return data

    def batch_create_order(self, params):
        url = '/open/api/mass_replaceV2'
        # params = {
        #     'symbol':symbol,
        #     'mass_place':[{
        #         'symbol':symbol,
        #         'side':side,
        #         'type':type,
        #         'volume':volume,
        #         'price':price,
        #         'fee_is_user_exchange_coin':0,
        #         }],}
        data = self.send_req('POST', url, params, issign=True)
        return data

    def batch_cancel_order(self, params):
        url = '/open/api/mass_replaceV2'
        # params = {
        #     'symbol':symbol,
        #     'mass_cancel':[
        #         1684047325184462848,
        #         1684045825066471424
        #         ],}
        data = self.send_req('POST', url, params, issign=True)
        return data

    def self_trade(self, params):
        url = '/open/api/self_trade'
        # params = {
        #     'symbol':'btcusdt',
        #     'side':'SELL',
        #     'type':1,
        #     'volume':1,
        #     'price':29400,
        #     }
        data = self.send_req('POST', url, params, issign=True)
        return data

    def open_order(self, symbol='btcusdt'):
        url = '/open/api/v2/new_order'
        params = {
            'symbol': symbol,
            # 'startDate':"2023-07-30 22:00:00",
            # 'endDate':"2023-07-30 23:22:00",
            'pageSize': 1000,
            # 'page':5,
        }
        data = self.send_req('GET', url, params, issign=True)
        return data

    def trade_record(self, params={}):
        url = '/open/api/all_trade'
        # params = {
        #     'symbol':symbol,
        #     'pageSize':pageSize,
        #     'page':page,
        #     }
        data = self.send_req('GET', url, params, issign=True)
        return data

    def bib_sign(self, path, act, params):
        self.time_sign = str(int((time.time()) * 1000))
        params1 = {
            'time': self.time_sign,
            'api_key': self.__api_key,
        }
        params1.update(params)
        if act == 'GET':
            if params == {}:
                sign = ''
                for key in sorted(params1.keys()):
                    sign += key + str(params1[key])
                response_data = sign + self.__secret_key
            else:
                sign = ''
                for key in sorted(params1.keys()):
                    sign += key + str(params1[key])
                response_data = sign + self.__secret_key
        elif act == 'POST':
            sign = ''
            for key in sorted(params1.keys()):
                sign += key + str(params1[key])
            response_data = sign + self.__secret_key
        self.string = response_data
        sign = hashlib.md5(response_data.encode("utf8")).hexdigest()
        self.sign = sign
        return sign


if __name__ == '__main__':
    api_key = ''
    secret_key = ''
    client = BIBrest(api_key, secret_key)
    data = client.get_ticker('btcusdt')
    print(data)
