import requests
import numpy as np 
import pandas as pd 

def get_weather():
    key = 'b8eb1022d4717675'
    place = 'WA/Seattle'
    url = 'http://api.wunderground.com/api/' + key + '/forecast/q/' + place + '.json'
    r = requests.get(url).json()
    weather = r['forecast']['simpleforecast']['forecastday'][0]

    data = dict()
    data['Min_TemperatureF'] = float(weather['low']['fahrenheit'])
    data['Max_Humidity'] = float(weather['maxhumidity'])
    data['Mean_Humidity '] = float(weather['avehumidity'])    
    data['Max_Wind_Speed_MPH '] = float(weather['maxwind']['mph'])
    data['Precipitation_In '] = float(weather['qpf_allday']['in'])


    return data
    

        
def get_bikes():
    bc = requests.get('https://secure.prontocycleshare.com/data/stations.json').json()
    current_time = pd.to_datetime(bc['timestamp'],unit='ms').tz_localize('UTC').tz_convert('US/Pacific')
    station_counts = [[i['n'],float(i['ba'])]for i in bc['stations']]
    df_sc = pd.DataFrame(station_counts, columns = ['terminal','bikes_avail'])

    return current_time, df_sc


def get_data(df_sc, current_time):
    all_times = pd.date_range(current_time, periods=24, freq='H')

    data_list = []

    df_sc['hour'] = -1
    df_sc['dayofweek'] = -1
    df_sc['month'] = -1
    df_sc = df_sc[['hour', 'terminal', 'Min_TemperatureF', 'Max_Humidity', 'Mean_Humidity ', 'Max_Wind_Speed_MPH ', 'Precipitation_In ', 'dayofweek', 'month']]
    
    for time in all_times:
        df_temp = df_sc.copy()


        df_temp['hour'] = time.hour
        df_temp['dayofweek'] = time.dayofweek
        df_temp['month'] = time.month
        df_temp['month'] = pd.Categorical(df_temp['month'], categories=range(1,13))
        df_temp['dayofweek'] = pd.Categorical(df_temp['dayofweek'], categories=range(7))
        df_temp['hour'] = pd.cut(df_temp['hour'],[-0.1,6,11,15,24])
        df_temp = pd.get_dummies(df_temp, columns = ['hour','terminal','dayofweek','month'])
        X = df_temp.values
        data_list.append(X)
    return data_list

def predict(rf, data_list):
    preds = []
    for X in data_list:
        preds.append(rf.predict(X))
    return preds


def totals(supply, demand, df_t):
    sim_data = []

    def avg_d(d):
        if d == 1:
            return 1.431767
        elif d == 2:
            return 4.299106
        elif d == 3:
            return 6.850962
        elif d == 4:
            return 12.680851
        else:
            return 0

    def avg_s(s):
        if s == 1:
            return 1.433981
        elif s == 2:
            return 4.298727
        elif s == 3:
            return 6.803055
        elif s == 4:
            return 12.15000
        else:
            return 0

    avg_s = np.vectorize(avg_s, otypes=[np.float])
    avg_d = np.vectorize(avg_d, otypes=[np.float])

    for s,d in zip(supply, demand):
        d_temp = df_t.copy()

        d_temp['bikes_avail'] = d_temp['bikes_avail'] - avg_d(d) + avg_s(s)
        d_temp['fill'] = d_temp['bikes_avail']/d_temp['dockcount']

        sim_data.append(d_temp.to_dict('records'))

    return sim_data




