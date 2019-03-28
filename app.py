import web
import ConfigParser
import pymysql
import json
import os

urls = (
    '/', 'Index',
    '/DBOutput', 'DBOutput',
    '/JsonOutput', 'JsonOutput',
    '/InputData', 'InputData',
    '/in','Login',
    '/out','Logout',
    '/page1','page1',
    '/images/(.*)', 'images' #this is where the image folder is located....
)

web.config.debug = False
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'privkey':None})    

# Read Configure
conf = ConfigParser.ConfigParser()
conf.read("config.conf")
#Databse definition
address = conf.get("MySQL Database", "address"   )        
account = conf.get("MySQL Database", "account"     )
password = conf.get("MySQL Database", "password"   )
datasheet = conf.get("MySQL Database", "datasheet"   )
#Template definition
template = conf.get("Template", "template" )
render = web.template.render(template)


class Login:
    def __init__(self):
        #Databse definition
        self.db = pymysql.connect(address, account, password, datasheet, charset="utf8")
        self.cursor = self.db.cursor()

    def GET(self):
        return self.render.SignIn() # ???

    def POST(self):
        i = web.input()
        usernumb = i.user
        password = i.password

        self.cursor.callproc('get_account')
        data = self.cursor.fetchall()
        print(data)
        dbuasr = data[0][0]
        dbpass = data[0][1]

        if usernumb == dbuasr and password ==dbpass:
            session.logged_in = True
            self.db.close()
            print()
            raise web.seeother('/page1') # ???
        else:
            session.logged_in = False
            self.db.close()
            raise web.seeother('/')
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

class Index:
    def __init__(self):
        pass
    def GET(self):
        return render.index()

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
        return render.index()

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

class Registered:
    def __init__(self):
        pass
    def GET(self):
        return render.Registered()

class Inquire:
    def __init__(self):
        pass
    def GET(self):
        return render.Inquire()

class Question:
    def __init__(self):
        pass
    def GET(self):
        return render.Question()

class QuestionStatus:
    def __init__(self):
        pass
    def GET(self):
        return render.QuestionStatus()

class PersonalInformation:
    def __init__(self):
        pass
    def GET(self):
        return render.PersonalInformation()

class Collection:
    def __init__(self):
        pass
    def GET(self):
        return render.Collection()


if __name__ == "__main__":
    app.run()
