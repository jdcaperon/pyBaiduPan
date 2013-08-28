#!/usr/bin/env python3.3    
# -*- coding:utf-8 -*-
###################################################
#A simple command-line client for Baidu Netdisk   #
#author:          Kather Lee                      #
#python version:  3.3                             #
#required packages:                               #
#    python-requests 1.2.3                        #
###################################################

import requests

KEY='Pfb12nmBr971bAaB33ubfXbp'
SEC='4ihI1zVf1tk2tjOEVUBxvQa35UZAf3xq'
APPNAME='PanLin'

def oauth_device(appkey, appsec):
    auth_url='https://openapi.baidu.com/oauth/2.0/device/code'
    device_para={'client_id' : appkey, 'response_type': 'device_code', 'scope': 'basic,netdisk'}
    res=requests.post(auth_url, device_para)
    device_json=res.json()
    #auth_err(device_json)
    print('''Follow these steps to complete authentication:
    1. Visit '''+ device_json['verification_url']+ ''' in your browser;
    2. Copy or input the following code when asked: '''+device_json['user_code']+'''
    3. After granted access permission, hit Enter to continue.
''')
    input('Hit [Enter] when finished... ')
    token_para={'grant_type': 'device_token', 'code': device_json['device_code'], 'client_id': appkey, 'client_secret': appsec}
    token_url='https://openapi.baidu.com/oauth/2.0/token'
    res=requests.post(token_url, token_para)
    token_json=res.json()
    #auth_err(token_json)
    return {'access_token': token_json['access_token'], 'refresh_token': token_json['refresh_token']}

def oauth_refresh(appkey, appsec, refresh_token):
    url="https://openapi.baidu.com/oauth/2.0/token"
    para={'grant_type': 'refresh_token', 'refresh_token': refresh_token, 'client_id': appkey, 'client_secret': appsec}
    res=requests.post(url, para)
    json=res.json()
    #auth_err(json)
    return {'access_token': json['access_token'], 'refresh_token': json['refresh_token']}

def get_quota(access_token):
    url='https://pcs.baidu.com/rest/2.0/pcs/quota'
    para={'method': 'info', 'access_token': access_token}
    res=requests.get(url,params=para)
    json=res.json()
    #api_err(json)
    return json

def list_file(access_token, path, appname):
    url='https://pcs.baidu.com/rest/2.0/pcs/file'
    para={'access_token': access_token, 'method': 'list', 'path': '/apps/'+appname+path}
    res=requests.get(url,params=para)
    json=res.json()
    #api_err(json)
    return json

