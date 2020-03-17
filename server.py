from flask import Flask, request, Response
from flask_restful import Resource, Api
from flask_cors import CORS
import json
import mysql.connector
import datetime

app = Flask(__name__)
CORS(app)
api = Api(app)


mydb = mysql.connector.connect(
        host = "", 
        user = "",
        passwd = "",
        database = ""
        )
cursor = mydb.cursor()



def addDB(title, description, start_date, end_date, username):
    sql = "insert into events(title, description, start_date, end_date, username) VALUES (%s, %s, %s, %s, %s)"
    val = (title, description, start_date, end_date,  username)
    cursor.execute(sql, val)
    mydb.commit()

def readDB():
    sql = "select title, description, start_date, end_date, username from events"
    cursor.execute(sql)
    L = []
    for(title, description, start_date, end_date, username) in cursor:
        L.append({'title': title , 'description': description, 'start_date': str(start_date), 'end_date': str(end_date), 'username': username})
    print(L)
    return(L)


def readDByear(year):
    sql = "select title, description, start_date, end_date, username from events where year(start_date) =" + str(year)
    cursor.execute(sql)
    L = []
    for(title, description, start_date, end_date, username) in cursor:
        L.append({'title': title , 'description': description, 'start_date': str(start_date), 'end_date': str(end_date), 'username': username})
    print(L)
    return(L)


def readDBmonth(year, month):
    sql = "select title, description, start_date, end_date, username from events where year(start_date) =" + str(year) + " and month(start_date) =" + str(month)
    cursor.execute(sql)
    L = []
    for(title, description, start_date, end_date, username) in cursor:
        L.append({'title': title , 'description': description, 'start_date': str(start_date), 'end_date': str(end_date), 'username': username})
    print(L)
    return(L)



def readDBday(year, month, day):
    sql = "select title, description, start_date, end_date, username from events where year(start_date) =" + str(year) + " and month(start_date) =" + str(month) + " and day(start_date) =" +str(day)
    cursor.execute(sql)
    L = []
    for(title, description, start_date, end_date, username) in cursor:
        L.append({'title': title , 'description': description, 'start_date': str(start_date), 'end_date': str(end_date), 'username': username})
    print(L)
    return(L)


def checkDuplicates(title, description, start_date, end_date, username):
    sql = "select title, description, start_date, end_date, username from events where title =" + "\'" + title + "\'" + " and description =" + "\'" + description + "\'" + " and start_date =" + "\'"+ start_date + "\'"+ " and end_date =" + "\'" + end_date + "\'"+  " and username =" + "\'" + username + "\'"
    print(sql)
    cursor.execute(sql)
    L = []
    for(title, description, start_date, end_date, username) in cursor:
        L.append({'title': title , 'description': description, 'start_date': str(start_date), 'end_date': str(end_date), 'username': username})
   
    return L

def delete(id):
    sql = 'delete from events where id = ' + str(id)
    cursor.execute(sql)
    mydb.commit()

class all_events(Resource):
    def get(self):
        year = None
        month = None
        day = None
        year = request.args.get('year')
        month = request.args.get('month')
        day = request.args.get('day')

        if year:
            if month:
                if day:
                    txt = json.dumps(readDBday(year, month, day))
                    resp = Response(txt, status=200, mimetype='application/json')
                    return resp

                else:
                    txt = json.dumps(readDBmonth(year, month))
                    resp = Response(txt, status=200, mimetype='application/json')
                    return resp
            else:
                txt = json.dumps(readDByear(year))
                resp = Response(txt, status=200, mimetype='application/json')
                return resp
        
        txt = json.dumps(readDB())
        # resp = Response(txt, status=200, mimetype='text/plain')
        resp = Response(txt, status=200, mimetype='application/json')
        return resp
        
    def post(self):
        print("recieved!") 
        event = request.get_json()
        print(request.get_json())
        dups = checkDuplicates(event['title'], event['description'], event['start_date'], event['end_date'], 'tony') 
        print(dups) 
        if len(dups) == 0:
             addDB(event['title'], event['description'], event['start_date'], event['end_date'], 'tony')
        
        #txt ={ "name": "tony",
               # "age": 12
               # }

       # resp = Response(txt, status=200, content_type='text/plain')
             result = {}
             result["result"] =  "success"
             resp = Response(json.dumps(result), status=200, mimetype='application/json')
        else:
             resp = Response("Error: event already exists!", status = 500, mimetype='text/plain')
        return resp

api.add_resource(all_events, '/events')



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)




