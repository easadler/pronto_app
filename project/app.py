from flask import Flask, render_template, request, jsonify

from bs4 import BeautifulSoup
import requests
import pandas as pd 
import numpy as np 
import json

app = Flask(__name__)

r = requests.get('https://secure.prontocycleshare.com/data/stations.json').json()
station_counts = [[i['n'],float(i['ba'])]for i in r['stations']]
df_sc = pd.DataFrame(station_counts, columns = ['terminal','bikes_avail'])

df = pd.read_csv('project/static/map/2015_station_data.csv')
df = df.merge(df_sc, on = 'terminal' )
terminals =  df.to_dict('records')



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
