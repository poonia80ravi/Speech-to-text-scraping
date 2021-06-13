from wit import Wit
import json
import random
import sys
import requests
import os
import glob
from multiprocessing import Pool
from multiprocessing import Process
from multiprocessing import Queue
from stem import Signal
from stem.control import Controller


WIT_API_HOST = os.getenv('WIT_URL', 'https://api.wit.ai')
WIT_API_VERSION = os.getenv('WIT_API_VERSION', '20200513')

with open('wit_token.json', 'r') as f:
    data = json.load(f)
    a = sys.argv[-3]
    tmp = data[a]
    b = tmp.split(',')


def func(token, w_file):
    
    proxies = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
    }
    with Controller.from_port(port = 9051) as c:
        c.authenticate()
        c.signal(Signal.NEWNYM)

    #print(requests.get('https://api.ipify.org', proxies=proxies).text)

    headers = {
        'authorization': 'Bearer ' + token,
        'accept': 'application/vnd.wit' + WIT_API_VERSION + '+json',
        'Content-Type': 'audio/wav'
    }
    full_url = WIT_API_HOST + '/speech'

    with open(w_file, 'rb') as f:
        data = f.read()

    r = requests.request('POST', full_url, headers=headers, proxies=proxies, data=data)
    temp = r.json()
    return temp

    '''client = Wit(token)
    resp = None
    with open(w_file, 'rb') as f:
        resp = client.speech(f, {'Content-Type': 'audio/wav', 'proxies': proxies})
    return resp'''


#with open('wit_token.json', 'r') as f:
    #data = json.load(f)
    #a = sys.argv[-3]
    #tmp = data[a]
    #b = tmp.split(',')
    #token = random.choice(b)
    #print(token)
'''
for i in glob.glob(sys.argv[-2]+'*.wav'):
    token = random.choice(b)
    print(token)
    
    dic = func(token, i)
    f_name = i.split('/')[-1]
    f_name1 = f_name.split('.')[0]
    f_name2 = f_name1+'.json'

    with open(sys.argv[-1]+f_name2, 'w') as f:
        json.dump(dic, f)
'''

def sample(f):
    token = random.choice(b)
    #print(token)

    dic = func(token, f)
    f_name = f.split('/')[-1]
    f_name1 = f_name.split('.')[0]
    f_name2 = f_name1+'.json'
    with open(sys.argv[-1]+f_name2, 'w') as f:
        json.dump(dic, f)

    

l = glob.glob(sys.argv[-2]+'*.wav')
#print(l)
#output = Queue()
#n = 2
#div = [l[i::n] for i in range(n)]
#print(div)
#processes = [Process(target=sample, args(div[i],output)) for i in range(n)]

#for p in processes:p.start()
#results = [output.get() for p in processes]
#print(results)
#for p in processes:p.join()
p = Pool(15)
results = list(p.imap(sample, l))
p.terminate()
p.join()



 
