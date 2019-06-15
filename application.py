from time import strptime
from datetime import datetime
from flask import Flask, render_template, request
import sqlite3 as sql
import pandas as pd
application = app = Flask(__name__)
import os
import sqlite3
from math import sin, cos, sqrt, atan2, radians
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import datetime
from datetime import timedelta
from datetime import datetime

#port = int(os.getenv("VCAP_APP_PORT"))
#port = os.getenv("VCAP_APP_PORT")

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def upload_csv():
   return render_template('upload.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
       con = sql.connect("database.db")
       csv = request.files['myfile']
       file = pd.read_csv(csv)
       file.to_sql('Earthquake', con, schema=None, if_exists='replace', index=True, index_label=None, chunksize=None, dtype=None)	  
       con.close()
       return render_template("result.html",msg = "Record inserted successfully")

@app.route('/list')
def list():
   con = sql.connect("database.db")
   cur = con.cursor()
   cur.execute("select * from Earthquake")
   
   rows = cur.fetchall();
   con.close()
   return render_template("list.html",data1 = rows)

@app.route('/magnitude')
def magnitude():
   return render_template('Magnitude.html')
   
@app.route('/options' , methods = ['POST', 'GET'])
def options():
   con = sql.connect("database.db")
 
   print (request.form['1'])
   print (request.form['1'])
   print (request.form['1'])
   print(request.form['mag'])
   cur = con.cursor()
   row = []
   rows_2 = []
   if request.form['1']== 'greater':
       cur.execute("select Count(*) from Earthquake where mag > ?",(request.form['mag'],))	   
       rows = cur.fetchall()
       cur.execute("select * from Earthquake where mag > ?",(request.form['mag'],))
       rows_2 = cur.fetchall()
   elif request.form['1']== 'lesser':
       cur.execute("select Count (*) from Earthquake where mag < ?",(request.form['mag'],))
       rows = cur.fetchall()
       cur.execute("select * from Earthquake where mag < ?",(request.form['mag'],))
       rows_2 = cur.fetchall()
   else :
       cur.execute("select Count (*) from Earthquake where mag = ?",(request.form['mag'],))
       rows = cur.fetchall()
       cur.execute("select * from Earthquake where mag = ?",(request.form['mag'],))
       rows_2 = cur.fetchall()
   print(len(rows))
   con.close()
   return render_template("list1.html",data = [rows,rows_2])

@app.route('/location')
def location():
   return render_template('Location.html')

if __name__ == '__main__':
    app.run(debug=True)


    #app.run(host='0.0.0.0', port=port)

   #app.run(debug=True)

    #app.run(host='127.0.0.1', port=port)
