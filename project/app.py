from flask import Flask, render_template, request, jsonify
from sklearn.externals import joblib
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np 
import json
import cPickle as pickle
import apidata as ap

app = Flask(__name__)


#df_sc = ap.get_data()
# get station data and merge with current data
# df = pd.read_csv('project/static/map/2015_station_data.csv')
# df = df.merge(df_sc, on = 'terminal' )
# terminals =  df.to_dict('records')

rf_d = joblib.load('project/static/pickles/demand pickle/d.pkl') 
rf_s = joblib.load('project/static/pickles/supply pickle/s.pkl') 






@app.route('/')
def index():
    return render_template('index.html', terminals = terminals)


@app.route('/simulation/', methods=['POST'])
def simulation():
	data = json.loads(request.form.get("data"))
	
	hour=  int(data['hour'])

	sim_data = []
	d_temp = df.copy()
	for _ in xrange(hour):
		d_temp['bikes_avail'] = d_temp['bikes_avail']  + np.random.rand() * 4 
		sim_data.append(d_temp.to_dict('records'))
	return jsonify(response = (sim_data))



if __name__ == '__main__':
	app.run(debug=True)
