#!/usr/bin/env python3.3    
# -*- coding:utf-8 -*-
###################################################
#A simple command-line client for Baidu Netdisk   #
#author:          Kather Lee                      #
#python version:  3.3                             #
#required packages:                               #
#    python-requests 1.2.3                        #
###################################################

import requests, hashlib, json, argparse, os, sys

KEY = 'Pfb12nmBr971bAaB33ubfXbp'
SEC = '4ihI1zVf1tk2tjOEVUBxvQa35UZAf3xq'
APPNAME = 'PanLin'

auth_url = 'https://openapi.baidu.com/oauth/2.0/device/code'
token_url = 'https://openapi.baidu.com/oauth/2.0/token'
quota_url = 'https://pcs.baidu.com/rest/2.0/pcs/quota'
file_url = 'https://pcs.baidu.com/rest/2.0/pcs/file'
cloud_url = 'https://psc.baidu.com/rest/2.0/pcs/services/cloud_dl'

def oauth_get_code(appkey, appsec):
    device_para = {'client_id' : appkey, 'response_type': 'device_code', 'scope': 'basic,netdisk'}
    res = requests.post(auth_url, device_para)
    device_json = res.json()
    auth_err(device_json)
    return device_json

def oauth_user_auth(url, user_code):
    print('''Follow these steps to complete authentication:
    1. Visit '''+ url + ''' in your browser;
    2. Copy or input the following code when asked: 
        ''' + user_code + '''
    3. After granted access permission, hit Enter to continue.
''')
    input('Hit [Enter] when finished... ')
    return True

def oauth_get_token(appkey, appsec, device_code):
    token_para = {'grant_type': 'device_token', 'code': device_code, 'client_id': appkey, 'client_secret': appsec}
    res = requests.post(token_url, token_para)
    token_json = res.json()
    auth_err(token_json)
    return {'access_token': token_json['access_token'], 'refresh_token': token_json['refresh_token']}

def oauth_refresh(appkey, appsec, refresh_token):
    para = {'grant_type': 'refresh_token', 'refresh_token': refresh_token, 'client_id': appkey, 'client_secret': appsec}
    res = requests.post(token_url, para)
    res_json = res.json()
    auth_err(res_json)
    return {'access_token': res_json['access_token'], 'refresh_token': res_json['refresh_token']}

def get_quota(access_token):
    para = {'method': 'info', 'access_token': access_token}
    res = requests.get(quota_url,params = para)
    res_json = res.json()
    api_err(res_json)
    return res_json

def list_file(access_token, r_path, by = None, order = None, limit = None):
    para = {'access_token': access_token, 'method': 'list', 'path': r_path}
    if by:
        para['by'] = by
    if order:
        para['order'] = order
    if limit:
        para['limit'] = limit
    res = requests.get(file_url,params = para)
    res_json = res.json()
    api_err(res_json)
    return res_json

def make_dir(access_token, r_path):
    para = {'access_token': access_token, 'method': 'mkdir', 'path': r_path}
    res = requests.post(file_url, params = para)
    res_json = res.json()
    api_err(res_json)
    return res_json

def file_info(access_token, r_path):
    para = {'access_token': access_token, 'method': 'meta', 'path': r_path}
    res = requests.get(file_url, params = para)
    res_json = res.json()
    api_err(res_json)
    return res_json

def move(access_token, from_path, to_path):
    para = {'access_token': access_token, 'method': 'move', 'from': from_path, 'to': to_path}
    res = requests.post(file_url, params = para)
    res_json = res.json()
    api_err(res_json)
    return res_json

def copy(access_token, from_path, to_path):
    para = {'access_token': access_token, 'method': 'copy', 'from': from_path, 'to': to_path}
    res = requests.post(file_url, params = para)
    res_json = res.json()
    api_err(res_json)
    return res_json

def delete(access_token, r_path):
    para = {'access_token': access_token, 'method': 'delete', 'path': r_path}
    res = requests.get(file_url, params = para)
    res_json = res.json()
    api_err(res_json)
    return res_json

def search(access_token, r_path, keyword, recursive = False):
    para = {'access_token': access_token, 'method': 'search', 'path': r_path, 'wd': keyword}
    if recursive:
        para['re'] = '1'
    res = requests.get(file_url, params = para)
    res_json = res.json()
    api_err(res_json)
    return res_json

def cloud(access_token, save_path, source_url, expires = False, rate_limit = False, timeout = False, callback = False):
    para = {'access_token': access_token, 'method': 'add_task', 'save_path': save_path, 'source_url': source_url}
    if expires:
        para['expires'] = expires
    if rate_limit:
        para['rate_limit'] = rate_limit
    if timeout:
        para['timeout'] = timeout
    if callback:
        para['callback'] = callback
    res = requests.post(cloud_url, params = para)
    res_json = res.json()
    api_err(res_json)
    return res_json

def download(access_token, r_path, l_path, chunksize = None):
    para = {'access_token':access_token, 'method': 'download', 'path': r_path}
    #To do: check if file exists
    size = file_info(access_token, r_path)['list'][0]['size']
    with open(l_path, 'wb') as f:
        if chunksize:
            pos = 0
            print('0.0%', end = '')
            while pos <= size:
                headers = {'range':'bytes=' + str(pos) + '-' + str(pos + chunksize - 1)}
                res= requests.get('https://d.pcs.baidu.com/rest/2.0/pcs/file', params = para, headers = headers)
                length = int(res.headers['Content-Length'])
                if pos <= size - chunksize and length < chunksize:
                    pass
#api_err(res.json())
                f.write(res.content)
                print('\r{:.1f}%'.format((pos + length)/size*100), end = '')
                pos+= chunksize
            print('\rDone')
        else:
            res = requests.get('https://d.pcs.baidu.com/rest/2.0/pcs/file', params = para)
            f.write(res.content)

def upload_single(access_token, r_path, l_path, ondup = 'overwrite'):
    para = {'access_token': access_token, 'path': r_path, 'method': 'upload', 'ondup': ondup}
    with open(l_path, 'rb') as f:
        res = requests.post('https://c.pcs.baidu.com/rest/2.0/pcs/file', params = para, files = {'file':f})
        res_json = res.json()
        api_err(res_json)
        return res_json

def upload_multiple(access_token, r_path, l_path, chunksize = 134217728, ondup = 'overwrite'):
    md5_list = []
    with open(l_path, 'rb') as f:
        while True:
            chunk = f.read(chunksize)
            para = {'access_token': access_token, 'method': 'upload', 'type': 'tmpfile'}
            res = requests.post('https://c.pcs.baidu.com/rest/2.0/pcs/file', params = para, files = {'file':chunk})
            res_json = res.json()
            api_err(res_json)
            md5_list.append(res_json['md5'])
            if(len(chunk) < chunksize):
                break
    httpbody = 'param='+json.dumps({'block_list':md5_list})
    para = {'access_token':access_token, 'method': 'createsuperfile', 'path': r_path, 'ondup': ondup}
    res = requests.post(file_url, params = para, data = httpbody.encode('utf-8'))
    res_json = res.json()
    api_err(res_json)
    return res_json

def api_err(res_json):
    print(res_json)

def auth_err(auth_json):
    print(auth_json)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init', action = "store_true", help = "Initialization")
    subparsers = parser.add_subparsers(title = 'commands', help = 'Usage', dest = 'command_name')
    parser_upload = subparsers.add_parser('upload', help = 'Upload single file')
    parser_upload.add_argument('LPATH', help = 'Local path')
    parser_upload.add_argument('RPATH', help = 'Remote path')
    parser_download = subparsers.add_parser('download', help = 'Download single file')
    parser_download.add_argument('RPATH', help = 'Remote path')
    parser_download.add_argument('LPATH', help = 'Local path')
    parser_download.add_argument('--multipart', '-m', action = "store_true", help = 'Multipart download')
    args = parser.parse_args()
    actk = ''
    if args.init:
        if os.path.isfile('.pybaidupan'):
            with open('.pybaidupan', 'r+') as f:
                lastactk = f.readline()
                refresh_token = f.readline().strip()
                tokens = oauth_refresh(KEY, SEC, refresh_token)
                actk = tokens['access_token']
                f.seek(0)
                f.truncate()
                f.write(tokens['access_token'] + os.linesep + tokens['refresh_token'])
        else:
            codes = oauth_get_code(KEY, SEC)
            if oauth_user_auth(codes['verification_url'], codes['user_code']):
                tokens= oauth_get_token(KEY, SEC, codes['device_code'])
                actk = tokens['access_token']
                with open('.pybaidupan', 'w') as f:
                    f.write(tokens['access_token'] + os.linesep + tokens['refresh_token'])
            else:
                print('Error!')
                sys.exit(1)
    elif os.path.isfile('.pybaidupan'):
        with open('.pybaidupan', 'r') as f:
            actk = f.readline().strip()
    else:
        print('Error')
        sys.exit(1)
    if args.command_name=='upload':
        upload_single(actk, args.RPATH, args.LPATH)
    elif args.command_name=='download':
        if args.multipart:
            download(actk, args.RPATH, args.LPATH, chunksize = 1024 * 1024)
        else:
            download(actk, args.RPATH, args.LPATH)

if __name__ == '__main__':
    main()
