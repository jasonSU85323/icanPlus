import configparser
import pymysql
import json
import time
from vault import MithVaultSDK

# Read Configure
conf = configparser.ConfigParser()
conf.read("config.conf")
#Databse definition
SQLtitle = "MySQL Database"
address = conf.get(SQLtitle, "address"   )        
account = conf.get(SQLtitle, "account"     )
password = conf.get(SQLtitle, "password"   )
datasheet = conf.get(SQLtitle, "datasheet"   )
db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
cursor = db.cursor()
#API definition
client_id  = conf.get("API definition", "client_id"    )
client_key = conf.get("API definition", "client_key"   )
mining_key = conf.get("API definition", "mining_key"   )
#Databse definition
db = pymysql.connect(host=address, port=3307, user=account, passwd=password, db=datasheet, charset='utf8')
cursor = db.cursor()
#Value definition
winner  = []
q_title = []
noReply = []


with open('log.json','r') as r:
    json_load = json.load(r)
r.close()


# Set winner
sql =   """
            SELECT q_title, q_people, a_people, Num, q_mithril
            FROM(
                    SELECT 
                            ROW_NUMBER() OVER(PARTITION BY q_title ORDER BY Rankingone ASC) AS Num,
                            Rankingone,
                            Rankingtwo,
                            q_title, 
                            q_people, 
                            a_people, 
                            sys_time ,
                            good,
                            q_mithril
                    FROM(
                            SELECT 
                                    Rankingone,
                                    DENSE_RANK() OVER(PARTITION BY q_title ORDER BY sys_time ) AS Rankingtwo, 
                                    q_title, 
                                    q_people, 
                                    a_people, 
                                    sys_time ,
                                    good,
                                    q_mithril
                            FROM (
                                    SELECT 
                                            RANK() OVER(PARTITION BY a_title ORDER BY good DESC) AS Rankingone, 
                                            q_title, 
                                            q_people, 
                                            a_people, 
                                            sys_time ,
                                            good,
                                            q_mithril
                                    FROM question, answer
                                    WHERE process=1 AND q_title=a_title
                                    ) AS AA
                            WHERE Rankingone<=3
                            ) AS BB
                    order by Rankingone, Rankingtwo
                    ) AS CC
            WHERE Num<=3
            order by q_title, Num
        """

cursor.execute(sql)
data = cursor.fetchall()

def set_reward(no, mithril):
    nostr = str(no)
    mithrilfloat = float(mithril)
    if nostr == '1':
        return round( mithrilfloat*0.5 ,2)
    elif nostr == '2':
        return round( mithrilfloat*0.3 ,2)
    elif nostr == '3':
        return round( mithrilfloat*0.2 ,2)

if data != None:
    for row in data:
        temp = {
            'q_title'   :row[0], 
            'q_people'  :row[1], 
            'a_people'  :row[2], 
            'no'        :row[3], 
            'reward'    :set_reward(row[3], row[4]),
            'q_mithril' :row[4]
        }
        winner.append(temp)

# Set q_title
if data != None:
    for row in data:
        q_title.append(row[0])
q_title = list(set(q_title))

# Set noReply
sql = 'SELECT q_people, q_mithril, q_title FROM question WHERE process=1'
cursor.execute(sql)
data2 = cursor.fetchall()
if data2 != None:
    for row in data2:
        if row[2] not in q_title:
            temp = {
                'q_people'   :row[0], 
                'q_mithril'  :row[1], 
                'q_title'    :row[2], 
            }
            noReply.append(temp)


if winner == [] and q_title == [] and noReply == []:
    exit()


# datatime = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
# logdata =   {
#                 'data': datatime,
#                 'winner':[],
#                 'AnsweredQuestion':[],
#                 'UnansweredQuestion':[]
#             }
# show

print()
print ("Recording time: ",time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
print("{:<46} {:<10} {:<10} {:<10} {:<10} {:<10}".format("q_title", "q_people", "a_people", 'no', "reward", 'q_mithril'))
for i in winner:
    print("{:<40} {:<10} {:<10} {:<10} {:<10} {:<10}".format(i['q_title'], i['q_people'] ,i['a_people'], i['no'], i['reward'], i['q_mithril']))
    # logdata['winner'].append([i['q_title'], i['q_people'] ,i['a_people'], i['no'], i['reward'], i['q_mithril']])
# exit()
# print("\nAnswered question:")
# for i in q_title:
#     print(i)
#     # logdata['AnsweredQuestion'].append([i])

# print("\nUnanswered question:")
# for i in noReply:
#     print(i['q_title'])
#     # logdata['UnansweredQuestion'].append([i])

# with open('log.json','w') as w:
#     json_load.append(logdata)
#     json.dump(json_load,w)
# w.close()


print()
# -------------------------------------------------------------------------------------------------------------------------------------
# Use the mining API to award rewards
MithVault = MithVaultSDK(client_id, client_key, mining_key)

for win in winner:
    sql = "SELECT token FROM member WHERE username=\'{}\'".format(win['a_people'])
    cursor.execute(sql)
    data = cursor.fetchone()

    if data[0] == None or data[0] == "":
        print("{:} no VAULT".format(win['a_people']))
        continue
    else:
        token  = data[0]
        reward = win['reward']
        result = MithVault.postUserMiningAction(token, reward)
        print("{:15} {:6} result is: {}".format(win['a_people'], win['reward'], result))
exit()
# ----------------------------------------------------------------------------------------------------------------------------------
# Release the process status of the database request
for t in q_title:
    sql = "UPDATE question SET process=\'\' WHERE AND q_title={}".format(t)
    cursor.execute(sql)
    db.commit()
for t in noReply:
    sql = "UPDATE question SET process=\'\' WHERE AND q_title={}".format(t['q_title'])
    cursor.execute(sql)
    db.commit()    
db.close()

# ----------------------------------------------------------------------------------------------------------------------------------
# Return the unanswered question to mith to the questioner
for t in noReply:
    sql = "UPDATE question SET process=\'\' WHERE AND q_title={}".format(t['q_title'])
    cursor.execute(sql)
    db.commit()

    sql = "SELECT token FROM member WHERE username=\'{}\'".format(t['q_people'])
    cursor.execute(sql)
    data = cursor.fetchone()
    token  = data[0]

    mith  = str(t['q_mithril'])

    result = MithVault.postUserMiningAction(token, mith)
    print("{:15} {:6} result is: {}".format(win['a_people'], win['reward'], result))


db.close()

# ----------END----------