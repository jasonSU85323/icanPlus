import web
import configparser
import pymysql
import json
import os
import json
import hmac
import requests
import time
import datetime
import string
from random import Random
import hashlib
import sys  
import uuid

from vault import MithVaultSDK
  

import importlib
importlib.reload(sys) 

urls = (
    '/','index',
    '/command/signUp', 'signUp',
    '/command/signIn','signIn',
    '/command/signOut','signOut',    
    '/command/inquire','inquire',
    '/command/postQuestion','postQuestion',
    '/link/question','question',
    '/link/profile','profile',
    '/link/favorite','favorite',
    '/event/setting','setting',
    '/event/answer', 'answer',
    '/link/favorite/add','favorite_add',
    '/link/favorite/del','favorite_del',
    '/like','like',

    '/about', 'about',

    '/success','success',
    '/faillure','faillure',
    '/success/donate','donateT',
    '/faillure/donate','donateF',

    '/link/vault','vault',
    '/event/addvault','addvault',
    '/event/delvault','delvault',
    
    '/inof','inof',
    '/test','test',
    '/test2','test2',
    '/test3','test3'
)
web.config.debug = False
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'logged_in': False, 'grant_code': False}) 

# def internalerror():
#     return  '''
#                 <script language="JavaScript">
#                     window.alert('User naem or email is already in use.');
#                     window.location.href='/';
#                 </script>
#             '''                  
# app.internalerror = internalerror


# Read Configure
conf = configparser.ConfigParser()
conf.read("config.conf")
#Databse definition
SQLtitle = "MySQL Database"
address = conf.get(SQLtitle, "address"   )        
account = conf.get(SQLtitle, "account"     )
password = conf.get(SQLtitle, "password"   )
datasheet = conf.get(SQLtitle, "datasheet"   )
#Template definition
template = conf.get("Template", "template" )
render = web.template.render(template)
#API definition
client_id  = conf.get("API definition", "client_id"    )
client_key = conf.get("API definition", "client_key"   )
mining_key = conf.get("API definition", "mining_key"   )
# 
tempuu = []





def nonce_random_str(randomlength=32):
    stra = ""
    chars = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        stra+=chars[random.randint(0, length)]
    return stra
def state_random_str(randomlength=3):
    stra = ""
    chars = "0123456789"
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        stra+=chars[random.randint(0, length)]
    return stra
def usernameToUUID(username):
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, username)).replace('-', '')

class inof:
    def GET(self):
        data1 = MithVaultSDK(client_id, client_key, mining_key).getClientInformation()
        print(json.dumps(data1, sort_keys=True, indent=4, separators=(',', ':')))

class test: # helpp
    def GET(self):
        token = '667481743143f17619e72e991bd17dc866e019506eb0cf2d27fa2d4d2421ce2edc3314a99a33f7a0935690e782465ccb8b2ae6830c41e67a81b2bf49fe524bf1'
        user_id = usernameToUUID('Linda')
        url = MithVaultSDK(client_id, client_key, mining_key).getDonateURI('20', mining_key, user_id)
        print(url)
        raise web.seeother(url)
        # http://haoyi.synology.me:8002/success/donate?state=4daaadf26d0cdf487d4f0929afbb81ee&uuid=703a6b74-f08a-45b6-a6bb-8bb956bf28b0&success=True

class test2: # helpp
    def GET(self):
        token = '667481743143f17619e72e991bd17dc866e019506eb0cf2d27fa2d4d2421ce2edc3314a99a33f7a0935690e782465ccb8b2ae6830c41e67a81b2bf49fe524bf1'
        data = MithVaultSDK(client_id, client_key, mining_key).postUserMiningAction(token, '3.14')
        print(data)
        # None
class test3:
    def GET(self):
        return  '''
                    <html>
                    <head>
                    <meta http-equiv="refresh" content="5;url=\'/\'"> 
                    </head>
                    <body>test 5s</body>
                    </html>
                '''

class addvault:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        i = web.input()
        username = i.username
        email    = i.email
        # print(username)
        # print(email)

        state = state_random_str()
        print("addvault: {}".format(state))

        sql = "UPDATE member SET state=\'{}\' WHERE username=\'{}\' AND email=\'{}\'".format(state, username, email)
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        self.db.close()

        url = MithVaultSDK(client_id, client_key, mining_key).getBindURI(state, usernameToUUID(username))
        raise web.seeother(url)

class delvault:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        i = web.input()
        username = i.username
        email    = i.email
        # print(username)
        # print(email)

        sql = "SELECT token FROM member WHERE username=\'{}\' AND email=\'{}\'".format(username, email)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        # print(data[0])

        re_code = MithVaultSDK(client_id, client_key, mining_key).deleteUserToken(data[0])
        print("re_code (None is del demo): {}".format(re_code))   # None is OK

        sql = "UPDATE member SET grant_code=\'{}\', state=\'{}\', token=\'{}\' WHERE username=\'{}\' AND email=\'{}\'".format("", "", "", username, email)
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        self.db.close()

        return  '''
                    <html>
                    <head>
                    <meta http-equiv="refresh" content="5;url=\'/link/vault\'"> 
                    </head>
                    <body>The VAULT license has been removed and jumps back to the page after 5 seconds.</body>
                    </html>
                '''

        # raise web.seeother('/link/vault')

class success:
    def __init__(self):
        #Databse definition    227
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        i = web.input()

        grant_code  = i.grant_code
        state       = i.state
        print("grant_code: {}\nstate: {}".format(grant_code, state))

        sql = "UPDATE member SET grant_code=\'{}\' WHERE state=\'{}\'".format(grant_code, state)
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()

        getToken = MithVaultSDK(client_id, client_key, mining_key).getAccessToken(grant_code, state)
        print("token :{}".format(getToken['token']))

        sql = "UPDATE member SET token=\'{}\' WHERE grant_code=\'{}\' AND state=\'{}\'".format(getToken['token'], grant_code, state)
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        self.db.close()        

        return  '''
                    <html>
                    <head>
                    <meta http-equiv="refresh" content="5;url=\'/link/vault\'"> 
                    </head>
                    <body>The VAULT authorization succeeds and jumps back to the page after 5 seconds.</body>
                    </html>
                '''


        # raise web.seeother('/link/vault')

class donateT:
    def __init__(self):    
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()    
    def GET(self):
        i = web.input()
        state = i.state
        uuid = i.uuid
        success = i.success
        print("state={}&uuid={}&success={}".format(state, uuid, success))
        if success == 'True':

            for i in tempuu:
                if i['session'] == session.session_id:
                    q_title     = i['q_title']
                    q_people    = i['q_people']
                    q_content   = i['q_content']
                    q_pro       = i['q_pro']
                    q_mithril   = i['q_mithril']
                    q_time      = i['q_time']

                    # print("{}\n{}\n{}\n{}\n{}\n{}".format(q_title, q_people, q_content, q_pro, q_mithril, q_time ))
                    # print("{}".format(q_mithril ))
                    # return "OK"
                    sql = "INSERT INTO question(q_title, q_people, q_content, q_pro, q_mithril, q_time, sys_time_s, sys_time_e) VALUES "
                    sql += "('{}','{}','{}','{}','{}','{}', NOW(), DATE_ADD(NOW(),INTERVAL 5 DAY))".format(q_title, q_people, q_content, q_pro, q_mithril, q_time)
                    # sql.decode('utf-8')
                    self.cursor.execute(sql)
                    self.db.commit()
                    self.db.close()
                    # raise web.seeother('/') # helpp
                    return  '''
                                <script language="JavaScript">
                                    window.alert('Your question has been sent.');
                                    window.location.href='/';
                                </script>
                            '''             
            # raise web.seeother('/')
        print("state={}&uuid={}&success={}".format(state, uuid, success))

class donateF:
    def GET(self):
        return  '''
                    <script language="JavaScript">
                        window.alert('VAULT ERROR');
                        window.location.href='/command/postQuestion';
                    </script>
                '''  
class faillure:
    def GET(self):
        i = web.input()
        print(i)
        return  '''
                    <html>
                    <head>
                    <meta http-equiv="refresh" content="5;url=\'/link/vault\'"> 
                    </head>
                    <body>The VAULT authorization failed and jumped back to the page after 5 seconds.</body>
                    </html>
                '''        

class vault:
    def __init__(self):
        #Value definition
        self.mode = {} 
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        sql = "SELECT username, email, password, callphone, homephone FROM member WHERE sessionid=\'{}\'".format(session.session_id)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        # print(data)
        if data == None:
            self.db.close()
            session.logged_in = False
            # return render.login('f', 'none')

            return  '''
                        <script language="JavaScript">
                            window.alert('Please login first');
                            window.location.href='/command/signIn';
                        </script>
                    '''      
        else:
            return render.vault('s', data[0], data[1], data[2], data[3], data[4])
    def POST(self):
        i = web.input()
        username = i.username
        email    = i.email

        sql = "SELECT token FROM member WHERE username=\'{}\' AND email=\'{}\'".format(username, email)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        self.db.close()
        # print(data)
        # print(data[0])
        if data[0] == None or data[0] == "":
            self.mode['static'] = 0
        else:
            token = data[0]
            data1 = MithVaultSDK(client_id, client_key, mining_key).getUserInformation(token)
            print(json.dumps(data1, sort_keys=True, indent=4, separators=(',', ':')))
            data2 = MithVaultSDK(client_id, client_key, mining_key).getClientInformation()
            print(json.dumps(data2, sort_keys=True, indent=4, separators=(',', ':')))

            self.mode = {}
            self.mode['static'] = 1
            self.mode['amount']        = data1['amount']
            self.mode['balance']       = data1['balance']
            self.mode['kyc_level']     = data1['kyc_level']
            self.mode['stake_level']   = data1['stake_level']
            self.mode['staked_amount'] = data1['staked_amount']
            self.mode['updated_at']    = data2[0]['updated_at']

        web.header('Content-Type', 'application/json')
        return json.dumps(self.mode)        

class index:
    def __init__(self):
        #Value definition
        self.mode = []        
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()

    def GET(self):
        sql = "SELECT username FROM member WHERE sessionid=\'{}\'".format(session.session_id)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()

        if data == None:
            self.db.close()
            session.logged_in = False
            return render.index('f', 'none')
        else:
            return render.index('s', data[0])

    def POST(self):  # SELECT * FROM question ORDER BY sys_time_s  LIMIT 10;
        i = web.input()

        sql = "SELECT q_title, q_content, q_people, q_pro, sys_time_e, ABS(TIME_TO_SEC(TIMEDIFF(sys_time_s, NOW()))) AS ElapsedTime FROM question ORDER BY sys_time_s  LIMIT 50"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for row in data:
            # print(row[5])
            v = {'q_title':row[0], 'q_content':row[1], 'q_people':row[2], 'q_pro':row[3], 'sys_time_e':row[4], 'ElapsedTime':int(float(row[5]))}
            # print(v)
            self.mode.append(v)
        self.db.close()
        # print(self.mode)
        web.header('Content-Type', 'application/json')
        return json.dumps(self.mode)

class signUp:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        return render.register('f', 'none')
    def POST(self):
        i = web.input()
        username    = i.username
        email       = i.email
        password    = i.password

        sql = "SELECT username FROM member WHERE username=\'{}\' OR email=\'{}\'".format(username, email)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        # print(data)
        if data != None:
            return  '''
                        <script language="JavaScript">
                            window.alert('User naem or email is already in use.');
                            window.location.href='/command/signUp';
                        </script>
                    '''                

        sql = "INSERT INTO member(username, email, password) VALUES (\'{}\', \'{}\', \'{}\')".format(username, email, password)
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        self.db.close()
        return  '''
                    <script language="JavaScript">
                        window.alert('registration success');
                        window.location.href='/command/signIn';
                    </script>
                '''           
        # raise web.seeother('/command/signIn')

class signIn:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        return render.login('f', 'none')
    def POST(self):
        i = web.input()
        email = i.email
        password = i.password
        sessionid  = session.session_id

        sql = "SELECT email, password FROM member WHERE email=\'{}\' AND password=\'{}\'".format(email, password)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        # print(data)
        try:
            db_email = data[0]
            db_password = data[1]
        except Exception as e:
            db_email = None

        if db_email == None:
            self.db.close()
            session.logged_in = False
            return  '''
                        <script language="JavaScript">
                            window.alert('Login failed');
                            window.location.href='/command/signIn';
                        </script>
                    '''               
            # raise web.seeother('/command/signIn')
        else:
            if db_email == email and db_password == password:
                sql = "UPDATE member SET sessionid=\'{}\' WHERE email=\'{}\' AND password=\'{}\'".format(sessionid, email, password)
                self.cursor.execute(sql)
                self.db.commit()                
                session.logged_in = True
                self.db.close()
                raise web.seeother('/')
            else:
                self.db.close()
                session.logged_in = False
                return  '''
                            <script language="JavaScript">
                                window.alert('Login failed');
                                window.location.href='/command/signIn';
                            </script>
                        '''                   
                # raise web.seeother('/command/signIn')

class signOut:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        sql = "UPDATE member SET sessionid=\'\' WHERE sessionid=\'{}\'".format(session.session_id) 
        self.cursor.execute(sql)
        self.db.commit()
        self.db.close()
        session.logged_in = False
        return  '''
                    <script language="JavaScript">
                        window.alert('Logged out');
                        window.location.href='/';
                    </script>
                '''                 
        # raise web.seeother('/')
 
class inquire:
    def __init__(self):
        #Value definition
        self.mode = []    
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        i = web.input()
        search = i.search
        sql = "SELECT username FROM member WHERE sessionid=\'{}\'".format(session.session_id)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()

        if data == None:
            self.db.close()
            session.logged_in = False
            return render.inquire('f', 'none', search)
        else:
            return render.inquire('s', data[0], search)

    def POST(self):
        i = web.input()
        search = i.search
        
        sql = "SELECT q_title, q_content, q_people, q_pro, sys_time_e, ABS(TIME_TO_SEC(TIMEDIFF(sys_time_s, NOW()))) AS ElapsedTime FROM question WHERE q_title LIKE \'%{}%\'".format(search)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for row in data:
            v = {'q_title':row[0], 'q_content':row[1], 'q_people':row[2], 'q_pro':row[3], 'sys_time_e':row[4], 'ElapsedTime':int(float(row[5]))}
            self.mode.append(v)
        self.db.close()
        # print(self.mode)
        web.header('Content-Type', 'application/json')
        return json.dumps(self.mode)

class postQuestion:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()

    def GET(self):
        sql = "SELECT username FROM member WHERE sessionid=\'{}\'".format(session.session_id)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()

        if data == None:
            self.db.close()
            session.logged_in = False
            return  '''
                        <script language="JavaScript">
                            window.alert('Please login first');
                            window.location.href='/command/signIn';
                        </script>
                    '''                
            # raise web.seeother('/command/signIn')
        else:
            return render.postquestion('s', data[0])

    def POST(self):
        i = web.input()
        q_title     = i.q_title
        q_people    = i.name
        q_content   = i.q_content
        q_pro       = i.q_pro
        q_mithril   = i.q_mithril
        q_time      = self.totimestr(int(time.time()))

        sql = "SELECT token FROM member WHERE username=\'{}\'".format(q_people)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        if data[0] == None or data[0] == "":
            print("{:} no VAULT".format(q_people))
            return  '''
                        <script language="JavaScript">
                            window.alert('You need to have a VAULT wallet license.');
                            window.location.href='/link/vault';
                        </script>
                    '''                            
            # raise web.seeother('/')
        else:
            tempuu.append(
                {   
                    'session'   :session.session_id,
                    'q_title'   :q_title,
                    'q_people'  :q_people,
                    'q_content' :q_content,
                    'q_pro'     :q_pro,
                    'q_mithril' :str(float(q_mithril)),
                    'q_time'    :q_time
                }
            )
            url = MithVaultSDK(client_id, client_key, mining_key).getDonateURI(str(float(q_mithril)*1.05), mining_key, "")
            print(url)
            raise web.seeother(url)


    def totimenum(self, timestr): 
        timeArray = time.strptime(timestr, "%Y-%m-%d %H:%M:%S")    
        timeStamp = int(time.mktime(timeArray))    
        return timeStamp

    def totimestr(self, timenum): 
        dateArray = datetime.datetime.utcfromtimestamp(timenum)    
        otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")    
        return otherStyleTime

class question:
    def __init__(self):
        #Value definition
        self.mode = []         
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        i = web.input()
        title = i.title
        user  = i.user
        print("------{}--{}".format(title,user))
        sql = "SELECT username FROM member WHERE sessionid=\'{}\'".format(session.session_id)
        self.cursor.execute(sql)
        data1 = self.cursor.fetchone()

        if data1 == None:
            session.logged_in = False
            sql = "SELECT q_content FROM question WHERE q_title=\'{}\'".format(title)
            self.cursor.execute(sql)
            data3 = self.cursor.fetchone()
            self.db.close()
            return render.question('f', 'none', title, data3[0], 0, 0)
        else:
            sql = "SELECT c_title, c_people FROM collection WHERE c_title=\'{}\' AND c_people=\'{}\'".format(title, user)
            self.cursor.execute(sql)
            data2 = self.cursor.fetchone()
            static = (0, 1)[data2 != None]

            sql = "SELECT q_content FROM question WHERE q_title=\'{}\'".format(title)
            self.cursor.execute(sql)
            data3 = self.cursor.fetchone()
            # print(data3)
            # data3_str = (0, data3)[data3 != None]      

            sql = "SELECT quota FROM member WHERE username=\'{}\'".format(user)       # helpp
            self.cursor.execute(sql)
            data4 = self.cursor.fetchone()
            # print(data4)
            # print(data4[0])
            quota = 1
            if data4 != None:
                if int(data4[0]) >= 10:
                    quota = 0
            # print(quota)
            print(data3[0])
            return render.question('s', data1[0], title, data3[0], static, quota)

    def POST(self):
        i = web.input()
        title = i.title
        user  = i.user

        sql = "SELECT a_people, a_content, ABS(TIME_TO_SEC(TIMEDIFF(sys_time, NOW()))) AS ElapsedTime FROM answer WHERE a_title=\'{}\'".format(title)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        sql = "SELECT v_people, v_title, v_to_content FROM vote WHERE v_people=\'{}\' AND v_title=\'{}\'".format(user, title)
        self.cursor.execute(sql)
        data2 = self.cursor.fetchone()
        # print(data2)
        # TF = ("", data2[2])[data2 != None]
        TF = None
        if data2 != None:
            TF = data2[2]
        print(TF)
        for row in data:
            v = {'a_people':row[0], 'a_content':row[1], 'ElapsedTime':int(float(row[2])), 'v_static':(0, 1)[row[1].replace('\r','').replace('\t','').replace('\n','') == TF]}
            self.mode.append(v)
            # print(row[0])
        self.db.close()
        print(self.mode)
        web.header('Content-Type', 'application/json')
        return json.dumps(self.mode)

class profile:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        sql = "SELECT username, email, password, callphone, homephone, points FROM member WHERE sessionid=\'{}\'".format(session.session_id)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        print(data)
        if data == None:
            self.db.close()
            session.logged_in = False
            return  '''
                        <script language="JavaScript">
                            window.alert('Please login first');
                            window.location.href='/command/signIn';
                        </script>
                    '''                
            # return render.login('f', 'none')
        else:
            return render.profile('s', data[0], data[1], data[2], data[3], data[4], data[5])

class favorite:
    def __init__(self):
        #Value definition
        self.mode = []            
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        sql = "SELECT username FROM member WHERE sessionid=\'{}\'".format(session.session_id)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()

        if data == None:
            self.db.close()
            session.logged_in = False
            return  '''
                        <script language="JavaScript">
                            window.alert('Please login first');
                            window.location.href='/command/signIn';
                        </script>
                    '''                 
            # return render.login('f', 'none')
        else:
            return render.favorite('s', data[0])
    def POST(self):
        i = web.input()
        name = i.name

        sql = "SELECT q_title, q_content, q_people, q_pro, sys_time_e, ABS(TIME_TO_SEC(TIMEDIFF(sys_time_s, NOW()))) AS ElapsedTime, q_mithril FROM question, collection WHERE c_people=\'{}\' AND c_title=q_title".format(name)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        for row in data:
            v = {'q_title':row[0], 'q_content':row[1], 'q_people':row[2], 'q_pro':row[3], 'sys_time_e':row[4], 'ElapsedTime':int(float(row[5])), 'q_mithril':row[6]}
            self.mode.append(v)
        self.db.close()
        # print(self.mode)
        web.header('Content-Type', 'application/json')
        return json.dumps(self.mode)

class setting:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()
    def GET(self):
        sql = "SELECT username, email, password, callphone, homephone FROM member WHERE sessionid=\'{}\'".format(session.session_id)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        print(data)
        if data == None:
            self.db.close()
            session.logged_in = False
            return  '''
                        <script language="JavaScript">
                            window.alert('Please login first');
                            window.location.href='/command/signIn';
                        </script>
                    ''' 
            # return render.login('f', 'none')
        else:
            return render.setting('s', data[0], data[1], data[2], data[3], data[4])
    def POST(self):
        i = web.input()
        email       = i.email
        username    = i.username
        email       = i.email
        password    = i.password
        callphone   = i.callphone
        homephone   = i.homephone

        # sql = "SELECT email, password FROM member WHERE email=\'{}\' AND password=\'{}\'".format(email, password)
        sql = "UPDATE member SET email=\'{}\', username=\'{}\', email=\'{}\', password=\'{}\', callphone=\'{}\', homephone=\'{}\' WHERE sessionid=\'{}\'".format(email, username, email, password, callphone, homephone, session.session_id) 
        self.cursor.execute(sql)
        self.db.commit()
        self.db.close()
        raise web.seeother('/link/profile')

class answer:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, use_unicode=True, charset='utf8')
        self.cursor = self.db.cursor()
    
    def POST(self):
        i = web.input()
        username    = i.username
        title       = i.title
        content     = i.content
        
        sql = "INSERT INTO answer(a_title, a_people, a_content, sys_time, good) VALUES "
        sql += "(\'{}\',\'{}\',\'{}\', NOW(), {})".format(title, username, content, 0)
        self.cursor.execute(sql)
        self.db.commit()
        self.db.close()
        return  '''
                    <script language="JavaScript">
                        window.alert('Answer completed.');
                        self.location=document.referrer;
                    </script>
                '''             
        raise web.seeother('/')

class favorite_add:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, use_unicode=True, charset='utf8')
        self.cursor = self.db.cursor()

    def GET(self):    
        i = web.input()
        name    = i.name 
        title   = i.title
        
        sql = "INSERT INTO collection(c_title, c_people) VALUES (\'{}\', \'{}\')".format(title, name) 
        # print(sql)
        self.cursor.execute(sql)
        self.db.commit()
        self.db.close()
        return  '''
                    <script language="JavaScript">
                        window.alert('Collection completed.');
                        self.location=document.referrer;
                    </script>
                '''
        # raise web.seeother(('/link/question?title={}&user={}'.format(title, name)).encode("utf-8").decode("latin1"))

    # def POST(self):
    #     i = web.input()
    #     name    = i.name 
    #     title   = i.title
        
    #     sql = "INSERT INTO collection(c_title, c_people) VALUES (\'{}\', \'{}\')".format(title, name) 
    #     # print(sql)
    #     self.cursor.execute(sql)
    #     self.db.commit()
    #     self.db.close()

    #     raise web.seeother(('/link/question?title={}&user={}'.format(title, name)).encode("utf-8").decode("latin1"))

class favorite_del:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()

    def GET(self):    
        i = web.input()
        name    = i.name 
        title   = i.title
        
        sql = "DELETE FROM collection WHERE c_title={}  AND c_people={}".format(title, name) 
        # print(sql)
        
        try:
            self.cursor.execute(sql)
        except Exception as e:
            print(e)
        self.db.commit()
        self.db.close()
        return  '''
                    <script language="JavaScript">
                        window.alert('Collection deleted.');
                        window.location.href='/link/favorite';
                    </script>
                '''             
        # raise web.seeother('/link/favorite')

    # def POST(self):
    #     i = web.input()
    #     name    = i.name 
    #     title   = i.title
        
    #     sql = "DELETE FROM collection WHERE c_title={}  AND c_people={}".format(title, name) 
    #     # print(sql)
    #     self.cursor.execute(sql)
    #     self.db.commit()
    #     self.db.close()

    #     raise web.seeother('/link/favorite')

class like:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()

    def GET(self):    
        i = web.input()
        name        = i.name
        title       = i.title
        a_content   = i.a_content

        sql = "SELECT v_people, v_title, v_to_content FROM vote WHERE v_people=\'{}\' AND v_title=\'{}\'".format(name, title)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        if data == None:
            sql = "INSERT INTO vote(v_people, v_title, v_to_content) VALUES (\'{}\', \'{}\', \'{}\')".format(name, title, a_content)
            # print(sql)
            self.cursor.execute(sql)
            self.db.commit()

            sql = "UPDATE answer SET good=good+1 WHERE a_title=\'{}\' AND a_content=\'{}\'".format(title, a_content)
            # print(sql)
            self.cursor.execute(sql)
            self.db.commit()

            sql = "UPDATE member SET quota=quota+1 WHERE username=\'{}\'".format(name)
            # print(sql)
            self.cursor.execute(sql)
            self.db.commit()
            
        else:
            sql = "UPDATE vote SET v_to_content=\'{}\' WHERE v_people=\'{}\' AND v_title=\'{}\'".format(a_content, name, title)
            # print(sql)
            self.cursor.execute(sql)
            self.db.commit()

            sql = "UPDATE answer SET good=good+1 WHERE a_title=\'{}\' AND a_content=\'{}\'".format(title, a_content)
            # print(sql)
            self.cursor.execute(sql)
            self.db.commit()

            sql = "UPDATE answer SET good=good-1 WHERE a_title=\'{}\' AND a_content=\'{}\'".format(title, data[2])
            # print(sql)
            self.cursor.execute(sql)
            self.db.commit()            
        
        self.db.close()
        return  '''
                    <script language="JavaScript">
                        window.alert('Voting completed.');
                        self.location=document.referrer;
                    </script>
                '''        
        # raise web.seeother(('/link/question?title={}&user={}'.format(title, name)).encode("utf-8").decode("latin1"))

    # def POST(self):
    #     i = web.input()
    #     name        = i.name
    #     title       = i.title
    #     a_people    = i.a_people

    #     sql = "SELECT v_people, v_title, v_to_content FROM vote WHERE v_people=\'{}\' AND v_title=\'{}\'".format(name, title)
    #     self.cursor.execute(sql)
    #     data = self.cursor.fetchone()
    #     if data == None:
    #         sql = "INSERT INTO vote(v_people, v_title, v_to_content) VALUES (\'{}\', \'{}\', \'{}\')".format(name, title, a_people)
    #         # print(sql)
    #         self.cursor.execute(sql)
    #         self.db.commit()
    #     else:
    #         sql = "UPDATE vote SET v_to_content=\'{}\' WHERE v_people=\'{}\' AND v_title=\'{}\'".format(name, title)
    #         # print(sql)
    #         self.cursor.execute(sql)
    #         self.db.commit()
        
    #     self.db.close()
    #     raise web.seeother('/link/question?title={}&user={}'.format(title, name))


class about:
    def __init__(self):
        #Value definition
        self.mode = []        
        #Databse definition
        self.db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
        self.cursor = self.db.cursor()

    def GET(self):
        sql = "SELECT username FROM member WHERE sessionid=\'{}\'".format(session.session_id)
        self.cursor.execute(sql)
        data = self.cursor.fetchone()

        if data == None:
            self.db.close()
            session.logged_in = False
            return render.about('f', 'none')
        else:
            return render.about('s', data[0])
if __name__ == "__main__":
    app.run()
