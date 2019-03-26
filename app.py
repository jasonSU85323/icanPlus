import web
import ConfigParser
import pymysql
import json

urls = (
    '/', 'index',
    '/DBOutput', 'DBOutput',
    '/JsonOutput', 'JsonOutput',
    '/InputData', 'InputData'
)

web.config.debug = False
app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'privkey':None})    

class Login:
    def __init__(self):
        #Value definition

        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        #Databse definition
        self.address = conf.get("MySQL Database", "address"   )        
        self.account = conf.get("MySQL Database", "account"     )
        self.password = conf.get("MySQL Database", "password"   )
        self.datasheet = conf.get("MySQL Database", "datasheet"   )
        self.db = pymysql.connect(self.address,self.account,self.password,self.datasheet,charset="utf8")
        self.cursor = self.db.cursor()
        #Template definition
        self.template = conf.get("Template", "template" )
        self.render = web.template.render(self.template)

    def GET(self):
        return self.render.SignIn() # ???

    def POST(self):
        i = web.input()
        usernumb = i.user
        password = i.password

        sql = "SELECT acc, pass FROM Account"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        dbuasr = data[0][0]
        dbpass = data[0][1]

        if usernumb == dbuasr and password ==dbpass:
            session.logged_in = True
            raise web.seeother('/CurrentState') # ???
        else:
            session.logged_in = False
            raise web.seeother('/')
class Logout:
    def GET(self):
        session.logged_in = False
        raise web.seeother('/')

class index:
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        #Template definition
        self.template 	= conf.get("Template", "template"	)
        self.render = web.template.render(self.template)
    def GET(self):
        print(self.template)
        return self.render.index()

class DBOutput:
    def __init__(self):
        #Value definition
        self.mode = [] 
        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        #Databse definition
        self.address = conf.get("MySQL Database", "address"   )        
        self.account = conf.get("MySQL Database", "account"		)
        self.password = conf.get("MySQL Database", "password"	)
        self.datasheet = conf.get("MySQL Database", "datasheet"   )
        self.db = pymysql.connect(self.address,self.account,self.password,self.datasheet,charset="utf8")
        self.cursor = self.db.cursor()
        #Template definition
        self.template = conf.get("Template", "template"	)
        self.render = web.template.render(self.template)

    def POST(self):
        sql = "SELECT acc, pass FROM Account"   
        print(sql)
        self.cursor.execute(sql)
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
        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        #Template definition
        self.template   = conf.get("Template", "template"   )
        self.render = web.template.render(self.template)
    def POST(self):
        i = web.input()
        print(i.test)        
        value = {   'A'   :'123',
                    'B'   :'456',
                    'C'   :'789'
                }        
        web.header('Content-Type', 'application/json')
        return json.dumps(value)
        return self.render.index()

class InputData:
    def __init__(self):
        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        #Template definition
        self.template = conf.get("Template", "template"   )
        self.render = web.template.render(self.template)

    def GET(self):
        i = web.input()
        print(i.t)
        return self.render.index()


if __name__ == "__main__":
    app.run()
