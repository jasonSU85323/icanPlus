import web
import ConfigParser
# import MySQLdb
import json

urls = (
    '/', 'index',
    '/DBOutput', 'DBOutput',
    '/JsonOutput', 'JsonOutput',
    '/InputData', 'InputData'
)

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

        conf = ConfigParser.ConfigParser()
        conf.read("config.conf")
        #Databse definition
        self.address = conf.get("MySQL Database", "address"   )        
        self.account = conf.get("MySQL Database", "account"		)
        self.password = conf.get("MySQL Database", "password"	)
        self.datasheet = conf.get("MySQL Database", "datasheet"   )
        self.db = MySQLdb.connect(address,account,password,datasheet,charset="utf8")
        self.cursor = self.db.cursor()
        #Template definition
        self.template = conf.get("Template", "template"	)
        self.render = web.template.render(self.template)

    def GET(self):
        sql = "SELECT acc, pass FROM Account"   
        print(sql)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        print(data)
        return self.render.index()

class JsonOutput:
    def __init__(self):
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
    app = web.application(urls, globals())
    app.run()
