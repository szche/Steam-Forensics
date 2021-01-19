import sqlite3
from jinja2 import Template, Environment, FileSystemLoader
from datetime import datetime

conn = sqlite3.connect('SteamLocal.db')
c = conn.cursor()

users = {}
messages = {}

# Collect users
for row in c.execute('SELECT * FROM Personas'):
    users[row[0]] = {
                'nick': row[1],
                'avatar': row[2]
            }


# Collect messages
for row in c.execute('SELECT * FROM Messages'):
    if row[1] not in messages:
        messages[row[1]] = [ users[row[1]]['nick'] ]
    if row[3] == 0:
        msgType = 'msgRcv'
    else:
        msgType = 'msgSent'
    messages[row[1]].append({
                'time': row[3],
                'utcTime': datetime.fromtimestamp(row[4]),
                'text': row[5],
                'isUnread': row[6],
                'isIncoming': row[7],
                'type': msgType
            })

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('temp.html')
output_from_parsed_template = template.render(users=users, messages=messages)

with open("index.html", "w") as fh:
    fh.write(output_from_parsed_template)
