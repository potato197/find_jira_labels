#! /usr/bin/env python3

import re
import ssl
import json
import sys
from urllib import request
from urllib.error import  URLError
from http import cookiejar
from login_jira import get_cookie

def get_label_list(jia_domain,filter_id):
    ssl._create_default_https_context = ssl._create_unverified_context

    header_dict = {'Content-Type': 'application/json'}
    data_url=jia_domain+"rest/gadget/1.0/piechart/generate?projectOrFilterId=filter-"+str(filter_id)+"&statType=labels&returnData=true"
    req = request.Request(url=data_url,headers=header_dict)

    login_result,cookie = get_cookie(jia_domain)
    if(login_result==False):
        print("Login failed.")
        return False,[]
        
    opener = request.build_opener(request.HTTPCookieProcessor(cookie))

    try:
        r = opener.open(req)
    except URLError as e:
        if hasattr(e, 'code'):
            print('Error code: ', e.code)
        if hasattr(e, 'reason'):
            print('Reason: ', e.reason)
        return False,[]
    res_str=r.read().decode('utf-8')
    res=json.loads(res_str)
    data_list=res.get('data')
    label_list=[]
    for data in data_list:
        label_list=label_list+[data.get('key')]
##    print(label_list)
    return True,label_list

def find_labels(jia_domain,filter_id,argv_list):
    print("jia_domain=%s" %(jia_domain))
    print("filter_id=%d" %(filter_id))
    result,label_list=get_label_list(jia_domain,filter_id)
    if(result==False):
        sys.exit()
    #print(label_list)
    print("Get list succeed!")

    result=[]
    for argv in argv_list:
        print('argv=%s'%(argv))
    #key_xxx
        rex="^"+argv+"_.+"
        pattern=re.compile(rex)
        for label in label_list:
            if pattern.match(label):
                result=result+[label]
    #xxx_key_xxx
        rex=".+_"+argv+"_.+"
        pattern=re.compile(rex)
        for label in label_list:
            if pattern.match(label):
                result=result+[label]
    #xxx_key
        rex=".+_"+argv+"$"
        pattern=re.compile(rex)
        for label in label_list:
            if pattern.match(label):
                result=result+[label]
    #key
        rex="^"+argv+"$"
        pattern=re.compile(rex)
        for label in label_list:
            if pattern.match(label):
                result=result+[label]
                break
    ##result=list(set(result))
    result.sort()
    print(result)

    fw = open("labels.txt", "w")
    fw.write(str(result))
    fw.close()

    out_list=""
    for sub_str in result:
        out_list=out_list+sub_str+"\n"
        
    fw = open("labels_list.txt", "w")
    fw.write(out_list)
    fw.close()

if __name__ == "__main__":
    jia_domain="https://idarttest.mot.com/"
    filter_id=136250 ###Please change to the real value.##
    argv_list = sys.argv[1:]
    if len(argv_list)==0:
        argv_list=['top']
    find_labels(jia_domain,filter_id,argv_list)
