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
    current_time = pd.to_datetime(bc['timestamp'],unit='ms')
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
        hour = time.hour
        dow = time.dayofweek
        month = time.month
        print df_temp
        df_temp['hour'] = hour
        df_temp['dayofweek'] = dow
        df_temp['month'] = month
        df_temp['hour'] = pd.cut(df_temp['hour'],[-0.1,6,11,15,24])
        df_temp = pd.get_dummies(df_temp, columns = ['hour','terminal','dayofweek','month'])
        
        X = df_temp.values
        data_list.append(X)