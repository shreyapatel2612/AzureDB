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


if __name__ == '__main__':
    app.run(debug=True)


    #app.run(host='0.0.0.0', port=port)

   #app.run(debug=True)

    #app.run(host='127.0.0.1', port=port)
