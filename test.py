import web
import ConfigParser
import pymysql
import json
import os

import hmac
import requests
import time
import string
from random import Random
import hashlib

from vault import MithVaultSDK

urls = (
    '/', 'test',
    '/DBOutput', 'DBOutput',
    '/JsonOutput', 'JsonOutput',
    '/InputData', 'InputData',
    '/in','Login',
    '/out','Logout',
    '/page1','page1',
    '/images/(.*)', 'images', #this is where the image folder is located....
    '/templetor','templetor',
    
    '/mithril/grant_code'   , 'grant_code',
    '/mithril/token'        , 'token',
    '/mithril/delete'        , 'delete',

    '/success','success',
    '/faillure','faillure',
)
web.config.debug = False
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'logged_in': None, 'grant_code': False, 'nonce' : False, 'timestamp' : False}) 

# Read Configure
conf = ConfigParser.ConfigParser()
conf.read("config.conf")
#Databse definition
address = conf.get("MySQL Database", "address"   )        
account = conf.get("MySQL Database", "account"     )
password = conf.get("MySQL Database", "password"   )
datasheet = conf.get("MySQL Database", "datasheet"   )
#Template definition
template = conf.get("Template test", "template" )
render = web.template.render(template)
#API definition
client_id  = "6d73661936a1d4f5d8e1fec12086dd20"
client_key = "b69af4646ceed2c1bbc44f9c0ac1f63c3edfeb4dc899b7bd38287ccb6791bcdb2d97f35ea6556dd5840ec7e7edf0cbf5e3bbf6e06e18a0e50a3fbf969e60c530"
mining_key = "demo"


def nonce_random_str(randomlength=32):
    str = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
def state_random_int(randomlength=3):
    str = ""
    chars = "0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return int(str)  
def sign_signature(payload, key):
    datalist = []
    
    for key, value in sorted(payload.items()):
        datalist.append("{}={}".format(key, value))

    data = '&'.join(datalist)
    print(data)
    return hmac.new(key, msg=data.encode(), digestmod=hashlib.sha512).hexdigest()

class success:
    def __init__(self):
        self.timestamp  = int(time.time())
        self.nonce      = nonce_random_str()
        self.state      = state_random_int()

    def GET(self):
        i = web.input()
        print(i.grant_code)

        # ccc = MithVaultSDK(client_id, client_key, mining_key).getAccessToken(i.grant_code, self.state)
        # print(ccc)
        # i = web.input()
        # session['grant_code']   = i.grant_code
        # grant_code      = i.grant_code
        # # print(grant_code)

        # S_payload = {    
        #     "client_id" : self.client_id,
        #     "nonce"     : self.nonce,
        #     "timestamp" : self.timestamp,
        # }
        # signature = sign_signature(S_payload, self.client_key.decode('hex'))

        # headers = {
        #   'X-Vault-Signature': signature,
        #   'Content-Type': 'application/json'
        # }
        # print(json.dumps(headers, sort_keys=True, indent=4, separators=(',', ':')))

        
        # payload = { 
        #             "client_id"     : self.client_id,
        #             "nonce"         : self.nonce,
        #             "timestamp"     : self.timestamp,
        #             "state"         : self.state,
        #             "grant_code"    : grant_code,
        # }
        # print(json.dumps(payload, sort_keys=True, indent=4, separators=(',', ':')))

        # url = "https://2019-hackathon.api.mithvault.io/oauth/token"
        # response = requests.post(url, headers=headers, data=json.dumps(payload), allow_redirects=False)
        
        # print("\n" + json.loads(response.text)['code'])
        # raise web.seeother('/')      

class faillure:
    def GET(self):
        i = web.input()
        print(i)
        return render.test()

class grant_code:
    def __init__(self):
        pass
        
    def GET(self):

        url = MithVaultSDK(client_id, client_key, mining_key).getBindURI(200)
        raise web.seeother(url)
        # url = "https://2019-hackathon.mithvault.io/#/oauth/authorize?client_id={}&state={}".format(self.client_id, 200)
        # print("\n" + url)
        # raise web.seeother(url)

class token:
    def __init__(self):
        self.timestamp  = int(time.time())
        self.nonce      = nonce_random_str()
        self.state      = state_random_int()

        self.grant_code = session.get('grant_code', None)
        print("\n" + self.grant_code)

    def GET(self):
        pass
        # S_payload = {    
        #     "client_id" : self.client_id,
        #     "nonce"     : self.nonce,
        #     "timestamp" : self.timestamp,
        # }
        # signature = sign_signature(S_payload, self.client_key.decode('hex'))

        # headers = {
        #   'X-Vault-Signature': signature,
        #   'Content-Type': 'application/json'
        # }
        # print(json.dumps(headers, sort_keys=True, indent=4, separators=(',', ':')))

        
        # payload = { 
        #             "client_id"     : self.client_id,
        #             "nonce"         : self.nonce,
        #             "timestamp"     : self.timestamp,
        #             "state"         : self.state,
        #             "grant_code"    : self.grant_code,
        # }
        # print(json.dumps(payload, sort_keys=True, indent=4, separators=(',', ':')))

        # url = "https://2019-hackathon.api.mithvault.io/oauth/token"
        # response = requests.post(url, headers=headers, data=json.dumps(payload), allow_redirects=False)
        
        # print("\n" + json.loads(response.text)['code'])
        # raise web.seeother('/')
    
class delete:
    def __init__(self):
        self.timestamp  = int(time.time())
        self.nonce      = nonce_random_str(32)
        self.state      = 300    
        
    def GET(self):
        pass
        # url = "https://2019-hackathon.api.mithvault.io/oauth/token?client_id={}&timestamp={}&nonce={}".format(self.client_id, self.timestamp, self.nonce)
        # print("\n" + url)
        # raise web.seeother(url)

















class test:
    def GET(self):
        return render.test()
class Logout:
    def __init__(self):
        pass
    def GET(self):
        session.logged_in = False
        raise web.seeother('/')
class page1:
    def __init__(self):
        pass
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/') 
        return render.page1()
class DBOutput:
    def __init__(self):
        #Value definition
        self.mode = [] 

        #Databse definition
        self.db = pymysql.connect(address, account, password, datasheet,charset="utf8")
        self.cursor = self.db.cursor()

    def POST(self):
        # sql = "SELECT acc, pass FROM Account"   
        # print(sql)
        # self.cursor.execute(sql)
        # data = self.cursor.fetchall()
        # print(data)
        
        self.cursor.callproc('get_account')
        data = self.cursor.fetchall()
        print(data)

        for row in data:
            v = {'acc':row[0], 'pass':row[1]}
            self.mode.append(v)
        self.db.close()

        web.header('Content-Type', 'application/json')
        return json.dumps(self.mode)
class JsonOutput:
    def __init__(self):
        #Value definition
        self.mode = []        
    def POST(self):
        i = web.input()
        print(i.test)        
        value = {   'A'   :'123',
                    'B'   :'456',
                    'C'   :'789'
                }        
        web.header('Content-Type', 'application/json')
        return json.dumps(value)
class InputData:
    def __init__(self):
        pass

    def GET(self):
        i = web.input()
        print(i.t)
        return render.test()
class images:
    def GET(self,name):
        ext = name.split(".")[-1] # Gather extension
        
        cType = {
            "png":"images/png",
            "jpg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"            }

        if name in os.listdir('images'):  # Security
            web.header("Content-Type", cType[ext]) # Set the Header
            return open('images/%s'%name,"rb").read() # Notice 'rb' for reading images
        else:
            raise web.notfound()
class templetor:
    def __init__(self):
        pass    
    def GET(self):
        return render.templetor('yoyoyo')

if __name__ == "__main__":
    app.run()
