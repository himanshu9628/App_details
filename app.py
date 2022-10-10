






from flask_apscheduler import APScheduler
# from flask import Flask, render_template,redirect,request,jsonify
# import time
from support import get_data as fun
import random
import sqlite3
import support
from datetime import datetime
from flask import Flask, render_template,redirect,request,jsonify
import json,requests
app = Flask(__name__)




scheduler = APScheduler()
scheduler.init_app(app)

app.apscheduler.add_job(func=fun, trigger='interval', seconds=604800,id=str(random.randint(1,3)))

scheduler.start()

def get_db_connection():
    conn = sqlite3.connect('appdetails.db')
    # conn.row_factory = sqlite3.Row
    conn.execute("create table IF NOT EXISTS APP_details (PackageId TEXT PRIMARY KEY, Running TEXT, Category TEXT , version TEXT, minos TEXT , install TEXT , developer TEXT )")
    # conn.execute("create table IF NOT EXISTS daycheck (Day TEXT PRIMARY KEY)")
    # print("Table created successfully")  
    return conn



@app.route('/appdata')
def Home():
    con = get_db_connection()
    cur = con.cursor() 
    query = '''SELECT * FROM APP_details'''
    cur.execute(query)  
    con.commit()
    rows = cur.fetchall() 
    # print(len(rows))
    # insert_rows = []
    # update_rows = []
    # print(rows)
    # dic = [dict(ix) for ix in rows]
    dic = {}



    for raw in rows:
        dic[raw[0]] = {}
        dic[raw[0]]['app_id'] = raw[0]
        try:
            dic[raw[0]]['category'] = raw[2]
        except:
            dic[raw[0]]['category'] = None
        try:
            dic[raw[0]]['Running'] = raw[1]
        except:
            dic[raw[0]]['Running'] = None
        try:
            dic[raw[0]]['version'] = raw[3]
        except:
            dic[raw[0]]['version'] = None
        try:
            dic[raw[0]]['minos'] = raw[4]
        except:
            dic[raw[0]]['minos'] = None
        try:
            dic[raw[0]]['install'] = raw[5]
        except:
            dic[raw[0]]['install'] = None
        try:
            dic[raw[0]]['developer'] = raw[6]
        except:
            dic[raw[0]]['developer'] = None

    return dic




  









if __name__ == '__main__':
    app.run(debug = True)
