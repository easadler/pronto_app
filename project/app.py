from flask import Flask, render_template, request, jsonify
from sklearn.externals import joblib
from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np 
import json
import cPickle as pickle
import apidata as ap


from apscheduler.scheduler import Scheduler

app = Flask(__name__)


cron = Scheduler(daemon=True)
# Explicitly kick off the background thread
cron.start()


@cron.interval_schedule(minutes=30)
def job_function():
 	# merge weather with stations 
	df_weather = pd.DataFrame([data for _ in xrange(len(df))])
	df_weather['terminal'] = df_t['terminal']

	#get list of datasets for each hour
	data_list = ap.get_data(df_weather, current_time)


	demand = ap.predict(rf_d, data_list)
	supply = ap.predict(rf_s, data_list)

	global sim_data
	sim_data = ap.totals(supply, demand, df_t)
	



@app.route('/')
def index():
	#get bike counts
	current_time, df_sc = ap.get_bikes()

	time_dict = {'hour': current_time.hour, 'minute': current_time.strftime('%M'), 'second': current_time.strftime('%S')}
	# get data to pass to view

	df_t = df.merge(df_sc, on = 'terminal', how= 'inner' )
	df_t['fill'] = df_t['bikes_avail']/df_t['dockcount']

	terminals =  df_t.to_dict('records')

	return render_template('index.html', terminals = terminals, time = time_dict)


@app.route('/simulation/', methods=['POST'])
def simulation():
	data = json.loads(request.form.get("data"))
	
	hour=  int(data['hour'])

	return jsonify(response = (sim_data[:hour]))



if __name__ == '__main__':

	df = pd.read_csv('project/static/map/reduced_station_data.csv')
	rf_d = joblib.load('project/static/pickles/demand pickle/d.pkl') 
	rf_s = joblib.load('project/static/pickles/supply pickle/s.pkl') 

	current_time, df_sc = ap.get_bikes()
	df_t = df.merge(df_sc, on = 'terminal', how= 'inner' )

	data = ap.get_weather()
	
	job_function()

	app.run(host='0.0.0.0',debug=True)
