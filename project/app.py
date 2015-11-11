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

@app.route('/')
def index():
	# get bike counts
	current_time, df_sc = ap.get_bikes()

	# get data to pass to view
	df_t = df.merge(df_sc, on = 'terminal' )
	terminals =  df_t.to_dict('records')

	# merge weather with stations 
	df_weather = pd.DataFrame([data for _ in xrange(len(terminals))])
	df_weather['terminal'] = df_t['terminal']

	# get list of times
	all_times = pd.date_range(current_time, periods=24, freq='H')
	
	#get list of datasets for each hour
	data_list = ap.get_data(df_weather, current_time)

	print data_list

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
	df = pd.read_csv('project/static/map/2015_station_data.csv')
	# rf_d = joblib.load('project/static/pickles/demand pickle/d.pkl') 
	# rf_s = joblib.load('project/static/pickles/supply pickle/s.pkl') 

	data = ap.get_weather()

	app.run(host='0.0.0.0',debug=True)
