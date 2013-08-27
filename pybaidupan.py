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

def oauth_device(appkey, appsec):
    auth_url='https://openapi.baidu.com/oauth/2.0/device/code'
    device_para={'client_id' : appkey, 'response_type': 'device_code', 'scope': 'basic,netdisk'}
    device_json=json.loads(api_req(auth_url, device_para, 'post'))
    #auth_err(device_json)
    print('''Follow these steps to complete authentication:
    1. Visit '''+ device_json['verification_url']+ ''' in your browser;
    2. Copy or input the following code when asked: '''+device_json['user_code']+'''
    3. After granted access permission, hit Enter to continue.
''')
    input('Hit [Enter] when finished... ')
    token_para={'grant_type': 'device_token', 'code': device_json['device_code'], 'client_id': appkey, 'client_secret': appsec}
    token_url='https://openapi.baidu.com/oauth/2.0/token'
    token_json=json.loads(api_req(token_url, token_para, 'post'))
    #auth_err(token_json)
    return {'access_token': token_json['access_token'], 'refresh_token': token_json['refresh_token']}

def oauth_refresh(appkey, appsec, refresh_token):
    token_url="https://openapi.baidu.com/oauth/2.0/token"
    refresh_para={'grant_type': 'refresh_token', 'refresh_token': refresh_token, 'client_id': appkey, 'client_secret': appsec}
    token_json=json.loads(api_req(token_url, refresh_para, 'post'))
    return {'access_token': token_json['access_token'], 'refresh_token': token_json['refresh_token']}

def get_quota(access_token):
    quota_url='https://pcs.baidu.com/rest/2.0/pcs/quota'
    quota_para={'method': 'info', 'access_token': access_token}
    quota_json=json.loads(api_req(quota_url, quota_para, 'get'))
    #api_err(quota_json)
    return quota_json

