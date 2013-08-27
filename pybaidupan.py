#!/usr/bin/env python3.3
# -*- coding:utf-8 -*-
#author: Kather Lee

import urllib.request, urllib.parse, json

KEY='Pfb12nmBr971bAaB33ubfXbp'
SEC='4ihI1zVf1tk2tjOEVUBxvQa35UZAf3xq'

def api_req(api_url, para_dict, method='post'):
    para=urllib.parse.urlencode(para_dict)
    if method == 'post':
        req=urllib.request.urlopen(api_url, para.encode('utf-8'))
    elif method == 'get':
        req=urllib.request.urlopen(api_url + '?' + para)
    else:
        raise Exception('Wrong request type.')
    return req.read().decode('utf-8')

def du_oauth_device(appkey, appsec):
    auth_url='https://openapi.baidu.com/oauth/2.0/device/code'
    device_para={'client_id' : appkey, 'response_type': 'device_code', 'scope': 'basic,netdisk'}
    device_json=json.loads(api_req(auth_url, device_para, 'post'))
    #du_err(device_json)
    print('''Follow these steps to complete authentication:
    1. Visit '''+ device_json['verification_url']+ ''' in your browser;
    2. Copy or input the following code when asked: '''+device_json['user_code']+'''
    3. After granted access permission, hit Enter to continue.
''')
    input('Hit [Enter] when finished... ')
    token_para={'grant_type': 'device_token', 'code': device_json['device_code'], 'client_id': BPCSU_KEY, 'client_secret': BPCSU_SEC}
    token_url='https://openapi.baidu.com/oauth/2.0/token'
    token_json=json.loads(api_req(token_url, token_para, 'post'))
    #du_err(token_json)
    
