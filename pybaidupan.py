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

auth_url='https://openapi.baidu.com/oauth/2.0/device/code'
token_url='https://openapi.baidu.com/oauth/2.0/token'
quota_url='https://pcs.baidu.com/rest/2.0/pcs/quota'
file_url='https://pcs.baidu.com/rest/2.0/pcs/file'
cloud_url='https://psc.baidu.com/rest/2.0/pcs/service/cloud_dl'

def oauth_device(appkey, appsec):
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
    res=requests.post(token_url, token_para)
    token_json=res.json()
    #auth_err(token_json)
    return {'access_token': token_json['access_token'], 'refresh_token': token_json['refresh_token']}

def oauth_refresh(appkey, appsec, refresh_token):
    para={'grant_type': 'refresh_token', 'refresh_token': refresh_token, 'client_id': appkey, 'client_secret': appsec}
    res=requests.post(token_url, para)
    json=res.json()
    #auth_err(json)
    return {'access_token': json['access_token'], 'refresh_token': json['refresh_token']}

def get_quota(access_token):
    para={'method': 'info', 'access_token': access_token}
    res=requests.get(quota_url,params=para)
    json=res.json()
    #api_err(json)
    return json

def list_file(access_token, r_path, by=None, order=None, limit=None):
    para={'access_token': access_token, 'method': 'list', 'path': r_path}
    if by:
        para['by']=by
    if order:
        para['order']=order
    if limit:
        para['limit']=limit
    res=requests.get(file_url,params=para)
    json=res.json()
    #api_err(json)
    return json

def make_dir(access_token, r_path):
    para={'access_token': access_token, 'method': 'mkdir', 'path': path}
    res=requests.post(file_url, para)
    json=res.json()
    #api_err(json)
    return json

def file_info(access_token, r_path):
    para={'access_token': access_token, 'method': 'meta', 'path': path}
    res=requests.get(file_url, params=para)
    json=res.json()
    #api_err(json)
    return json

def move(access_token, from_path, to_path):
    para={'access_token': access_token, 'method': 'move', 'from': from_path, 'to': to_path}
    res=requests.post(file_url, para)
    json=res.json()
    #api_err(json)
    return json

def copy(access_token, from_path, to_path):
    para={'access_token': access_token, 'method': 'copy', 'from': from_path, 'to': to_path}
    res=requests.post(file_url, para)
    json=res.json()
    #api_err(json)
    return json

def delete(access_token, r_path):
    para={'access_token': access_token, 'method': 'delete', 'path': r_path}
    json=res.json()
    #api_err(json)
    return json

def search(access_token, r_path, keyword, recursive=False):
    para={'access_token': access_token, 'method': 'search', 'path': r_path, 'wd': keyword}
    if recursive:
        para['re']='1'
    res=requests.get(file_url, params=para)
    json=res.json()
    #api_err(json)
    return json

def cloud(access_token, save_path, source_url, expires=False, rate_limit=False, timeout=False, callback=False):
    para={'access_token': access_token, 'method': 'add_task', 'save_path': save_path, 'source_url': source_url}
    if expires:
        para['expires']=expires
    if rate_limit:
        para['rate_limit']=rate_limit
    if timeout:
        para['timeout']=timeout
    if callback:
        para['callback']=callback
    res=requests.post(cloud_url, para)
    json=res.json()
    #api_err(json)
    return json

