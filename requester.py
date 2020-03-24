import random
import requests
import time
from config import *

from utils import converter,getVar
import config

def requester(url,data,headers,GET,delay,timeout):
    if getVar('jsondata'):
        data=convert(data)
    elif getVar('path'):
        url=convert(data,url)
        data=[]
        GET,POST=True,False
    time.sleep(delay)
    user_agents = ['Mozilla/5.0 (X11; Linux i686; rv:60.0) Gecko/20100101 Firefox/60.0',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                   'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.991']
    if 'User-Agent' not in headers:
        headers['User-Agent'] = random.choice(user_agents)
    elif headers['User-Agent'] == '$ ':
        headers['User-Agent'] = random.choice(user_agents)
    
    requests.packages.urllib3.disable_warnings()
    if GET:
        response=requests.get(url,params=data,headers=headers,timeout=timeout,verify=False)
    elif getVar('jsondata'):
        response=requests.post(url,json=data,headers=headers,timeout=timeout,verify=False)
    else:
        response=requests.post(url,data=data,headers=headers,timeout=timeout,verify=False)
    return response


# url='http://123.206.87.240:8002/get/'
# data=''
# headers=config.headers
# delay=config.delay
# timeout=config.timeout
# response=requester(url,data,headers,True,delay,timeout).text
# print(response)












