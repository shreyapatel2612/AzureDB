import string

from flask import Flask, render_template, request
import pyodbc
import os
import redis
import time
import random
import redis
from math import sin, cos, sqrt, atan2, radians

application = app = Flask(__name__)

# port = int(os.getenv("VCAP_APP_PORT", '5000'))
# port = os.getenv("VCAP_APP_PORT")


myHostname = "freebird.redis.cache.windows.net"
myPassword = "Rz1ycTO3oebJcgLJRIdLUrJZAveKitHsJ0gJhat6QNs="

r = redis.StrictRedis(host=myHostname, port=6380, password=myPassword, ssl=True)

result = r.ping()
print("Ping returned : " + str(result))

server = 'mysqlserver6429.database.windows.net'
database = 'MyDB'
username = 'shreya6429'
password = 'Myaccount@123'
driver = '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect(
    'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)


@app.route('/')
def home():
    return render_template('home.html')


#     cursor = cnxn.cursor()
#     cursor.execute("SELECT * FROM people")
#     row = cursor.fetchall()
# return render_template('home.html', data=row)


@app.route('/options', methods=['POST', 'GET'])
def options():
    start_time = time.time()
    num = int(request.form['num'])
    rows = []
    c = []
    for i in range(num):
        val = round(random.uniform(2, 5), 1)
        cur = cnxn.cursor()
        a = 'select * from all_months WHERE mag = ' + str(val)
        v = str(val)
        if r.get(a):
            print('Cached')
            c.append('Cached')
        else:
            print('Not Cached')
            c.append('Not Cached')
            cur.execute("select * from all_months WHERE mag = ?", (val,))
            get = cur.fetchall();
            r.set(a, str(get))
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template("list1.html", rows=[c], elapsed_time=elapsed_time)


@app.route('/options2', methods=['POST', 'GET'])
def options2():
    start_time = time.time()
    num = int(request.form['num'])
    loc = (request.form['loc'])
    rows = []
    for i in range(num):
        cur = cnxn.cursor()
        b = "select * from all_months WHERE place LIKE ? '%'" + loc + "%"
        # cur.execute("select * from all_months WHERE place LIKE  '"+ ('%' + loc + '%',))
        # get = cur.fetchall();

        if r.get(b):
            rows.append(r.get(b))
            print('Cached')
        else:
            print('Not Cached')
            cur.execute("select * from all_months WHERE place LIKE ?", ('%' + loc + '%',))
            get = cur.fetchall();
            rows.append(get)
            r.set(b, str(get))
    end_time = time.time()
    elapsed_time = end_time - start_time
    r.flushdb()
    return render_template("list1.html", rows=[rows], elapsed_time=elapsed_time)


@app.route('/distance', methods=['POST', 'GET'])
def distance():
    start_time = time.time()
    print(float(request.form['lat1']))
    print(float(request.form['lon1']))
    print(float(request.form['kms']))
    lat1 = float(request.form['lat1'])
    lon1 = float(request.form['lon1'])
    cur = cnxn.cursor()
    b = "select * from all_months where latitude  = " + request.form['lat1'] + " and longitude = " + request.form[
        'lon1'] + "'"
    # cur.execute("select * from all_months ")
    # rows = cur.fetchall()
    # ref:https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    R = 6373.0

    dist = []
    rows = []
    if r.get(b):
        if (r.get(b) <= (float(request.form['kms']))):
            print("cache")

    else:
        cur.execute("select * from all_months where latitude  = ? and longitude = ?",
                    (request.form['lat1'], request.form['lon1'],))
        get = cur.fetchall();
        lat_r = radians(float(request.form['lat1']))
        lon_r = radians(float(request.form['lon1']))
        print(len(get))
        for row in get:
            lat2 = radians(row[2])
            lon2 = radians(row[3])
            dlon = lon2 - lon_r
            dlat = lat2 - lat_r
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance = float(R * c)
            if (distance <= (float(request.form['kms']))):
                dist.append(row)
                r.set(b, distance)
            #rows.append(get)

    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template("list1.html", elapsed_time=elapsed_time, rows=[dist])


@app.route('/timerange', methods=['POST', 'GET'])
def timerange():
    start_time = time.time()
    num = int(request.form['num'])
    time1 = request.form['time1']
    time2 = request.form['time2']
    rows = []
    for i in range(num):
        cur = cnxn.cursor()
        b = "select * from all_months WHERE time BETWEEN %" + time1 + "% and %" + time2 + "%"
        cur.execute("select * from all_months WHERE time BETWEEN ? and ?", (time1, time2))
        get = cur.fetchall()
        rows.append(get)
        if r.get(b):
            print('Cached')
        else:
            print('Not Cached')
            # cur.execute("select * from all_month WHERE place LIKE ?", ('%'+loc+'%',))
            # get = cur.fetchall();
            r.set(b, str(get))
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template("list1.html", rows=[rows], elapsed_time=elapsed_time)

############ restricted mag range #############

@app.route('/options3', methods=['POST', 'GET'])
def options3():
    start_time = time.time()
    num = int(request.form['num'])
    mag1 = float(request.form['mag1'])
    mag2 = float(request.form['mag2'])
    rows = []
    c = []
    for i in range(num):
        val = round(random.uniform(mag1, mag2), 1)
        cur = cnxn.cursor()
        a = 'select * from all_months WHERE mag = ' + str(val)
        v = str(val)
        if r.get(a):
            print('Cached')
            c.append('Cached')
        else:
            print('Not Cached')
            c.append('Not Cached')
            cur.execute("select * from all_months WHERE mag = ?", (v,))
            get = cur.fetchall()
            r.set(a, str(get))
    end_time = time.time()
    elapsed_time = end_time - start_time
    return render_template("list1.html", rows=[c], elapsed_time=elapsed_time)

################# Without Redis ################

@app.route('/quiz36', methods=['POST', 'GET'])
def quiz36():
    start_time = time.time()
    num = int(request.form['num'])
    loc = (request.form['loc'])
    rows = []
    d = []
    for i in range(num):
        letter = random.choice(string.ascii_lowercase)
        str = loc + letter
        cur = cnxn.cursor()
        cur.execute("select * from all_months WHERE net = ?", str )
        get = cur.fetchall()
        rows.append(get)
    end_time = time.time()
    print(rows)
    elapsed_time = end_time - start_time
    return render_template("list1.html", rows=rows, elapsed_time=elapsed_time)


################# With Redis ################
@app.route('/quiz36r' , methods = ['POST', 'GET'])
def quiz36r():
   start_time = time.time()
   num =int(request.form['num'])
   loc = (request.form['loc'])
   rows = []
   d =[]
   for i in range(num):
       val = random.choice(string.ascii_lowercase)
       net = loc + val
       cur = cnxn.cursor()
       b = 'select * from all_months WHERE net LIKE ' +str(net)+ '%'
       cur.execute("select * from all_months WHERE net LIKE ?", (net+'%',))
       get = cur.fetchall()
       rows.append(get)
       if r.get(b):
           print ('Cached')
           d.append('Cached')
       else:
           print('Not Cached')
           d.append('Not Cached')
           r.set(b,str(get))
   end_time = time.time()
   elapsed_time = end_time - start_time
   print (elapsed_time)
   return render_template("list1.html",rows = rows,elapsed_time=elapsed_time)

if __name__ == '__main__':
    app.run(debug=True)

# app.run(host='0.0.0.0', port=port)
# app.run(host='127.0.0.1', port=port)
