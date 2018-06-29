#! /usr/bin/env python3

import ssl
import json
from urllib import request
from urllib.error import  URLError
from http import cookiejar

def load_cookie_from_file(filename):
    print("load_cookie_from_file")
    cookie = cookiejar.MozillaCookieJar()
    try:
        cookie.load(filename, ignore_discard=True, ignore_expires=True)
    except Exception as e:
        print("Load cookie error.")
        if hasattr(e, 'errno'):
            print('errno: ', e.errno)
        if hasattr(e, 'winerror'):
            print('winerror: ', e.errno)
        if hasattr(e, 'strerror'):
            print('strerror', e.strerror)
        return None
    return cookie

def update_cookie_to_file(cookie_filename,account_filemane,session_str,header_dict):
    print("update_cookie_to_file")

    default_loginData={
            "username": "Your username",
            "password": "xxx"
        }
    load_account_info_failed=False
    try:
        fr = open(account_filemane, "r")
        loginData = json.load(fr)
    except Exception as e:
        load_account_info_failed=True
        print("Load account info error.")
        if hasattr(e, 'errno'):
            print('errno: ', e.errno)
        if hasattr(e, 'winerror'):
            print('winerror: ', e.errno)
        if hasattr(e, 'strerror'):
            print('strerror', e.strerror)
    else:
        fr.close()
    
    if ((load_account_info_failed==False) and ('username' in loginData) and ('password' in loginData)):
        print("Read account info from file succeed:\n%s" % str(loginData))
        loginData = json.dumps(loginData).encode(encoding='utf-8')
    else:
        if(load_account_info_failed==False):
            print("Invalid account info, loginData=%s" % str(loginData))
            print("Please check your account info in file:%s" % account_filemane)
        else:
            fw = open(account_filemane, "w")
            json.dump(default_loginData, fw)
            fw.close()
            print("Please save your account info into file:%s" % account_filemane)
        return None

    req = request.Request(url=session_str,data=loginData,headers=header_dict)

    cookie = cookiejar.MozillaCookieJar(cookie_filename)
    opener = request.build_opener(request.HTTPCookieProcessor(cookie))
    try:
        r = opener.open(req)
    except URLError as e:
        print("Update cookie error.")
        if hasattr(e, 'code'):
            print('Error code: ', e.code)
        if hasattr(e, 'reason'):
            print('Reason: ', e.reason)
        return None
    print('Get cookie succeed!')
    cookie.save(ignore_discard=True, ignore_expires=True)
    return cookie

def get_cookie(domain):
    ssl._create_default_https_context = ssl._create_unverified_context
    cookie_filename="cookie.txt"
    account_filemane="account.json"
    header_dict = {'Content-Type': 'application/json'}
    session_str=domain+"rest/auth/1/session"
    
    req = request.Request(url=session_str,headers=header_dict)

    cookie = load_cookie_from_file(cookie_filename)
    if cookie==None:
        cookie = update_cookie_to_file(cookie_filename,account_filemane,session_str,header_dict)
    if cookie==None:
        print('Login error:%s' % "cookie==None")
        return False,None
    opener = request.build_opener(request.HTTPCookieProcessor(cookie))

    cookie_expired_error=False

    try:
        r = opener.open(req)
    except URLError as e:
        if hasattr(e, 'code'):
            print('Error code: ', e.code)
            if e.code==401:
                cookie_expired_error=True
        if hasattr(e, 'reason'):
            print('Reason: ', e.reason)
        if cookie_expired_error==False:
            print('Login error:%s' % "URLError")
            return False,None
    if cookie_expired_error==True:
        cookie_expired_error=False
        cookie = update_cookie_to_file(cookie_filename,account_filemane,session_str,header_dict)
        if cookie==None:
            print('Login error:%s' % "cookie==None 2")
            return False,None
        opener = request.build_opener(request.HTTPCookieProcessor(cookie))
        req = request.Request(url=session_str,headers=header_dict)
        try:
            r = opener.open(req)
        except URLError as e:
            if hasattr(e, 'code'):
                print('Error code: ', e.code)
            if hasattr(e, 'reason'):
                print('Reason: ', e.reason)
            print('Login error:%s' % "URLError 2")
            return False,None

    res_str=r.read().decode('utf-8')
    res=json.loads(res_str)
    if 'errorMessages' in res:
        print('Login error:%s' % res.get('errorMessages'))
        return False,None
    else:
##        print('Login succeed!\nres=\n%s' % res)
        print('Login succeed!')
        return True,cookie

if __name__ == "__main__":
    get_cookie(r"https://idarttest.mot.com/")
    
