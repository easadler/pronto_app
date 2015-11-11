import requests
import numpy as np 
import pandas as pd

def get_data():
    
    def get_weather(year, month, day):
        datetime = str(year) + str(month) + str(day)
        key = 'b8eb1022d4717675'
        place = 'WA/Seattle'
        url = 'http://api.wunderground.com/api/' + key + '/history_' + datetime + '/q/' + place + '.json'
        r = requests.get(url).json()
        weather = r['history']['dailysummary'][0]
        return weather
        current_time, df_sc = get_bikes()
        
    def get_bikes():
        bc = requests.get('https://secure.prontocycleshare.com/data/stations.json').json()
        current_time = pd.to_datetime(bc['timestamp'],unit='ms')

        station_counts = [[i['n'],float(i['ba'])]for i in bc['stations']]
        df_sc = pd.DataFrame(station_counts, columns = ['terminal','bikes_avail'])

        return current_time, df_sc
    
    # get important days 
    current_time, df_sc = get_bikes()


    hour = current_time.hour
    dow = current_time.dayofweek
    month = current_time.month
    
    weather = get_weather(current_time.year, month, current_time.day)
    
    data = dict()
    
    data['Max_Humidity'] = weather['maxhumidity']
    data['Max_Wind_Speed_MPH '] = weather['maxwspdm']
    data['Min_Dewpoint_F'] = weather['mindewpti']
    data['Max_Wind_Speed_MPH '] = weather['maxwspdi']
    data['Mean_Humidity '] = weather['humidity']
    data['Precipitation_In '] = weather['precipi']
    data['Min_TemperatureF'] = weather['mintempi']
    data['hour'] = hour
    data['dayofweek'] = dow
    data['month'] = month
    
    
    df_d = pd.DataFrame([data for _ in xrange(len(df_sc))])

    df_sc = df_sc.merge(df_d, left_index =True, right_index = True)
    
    return df_sc
    
    