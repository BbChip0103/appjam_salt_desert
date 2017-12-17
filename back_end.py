# -*- coding: utf8 -*-

import urllib.request
import json
import pymysql
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

import config

app = Flask(__name__)
CORS(app)

conn = pymysql.connect(host=config.DB_CONFIG['host'],
                        user=config.DB_CONFIG['user'],
                        password=config.DB_CONFIG['password'],
                        db=config.DB_CONFIG['db'],
                        charset='utf8')
curs = conn.cursor(pymysql.cursors.DictCursor)

base_url = 'http://api.openweathermap.org/data/2.5/weather?'
location = 'lat=20.13378&lon=67.48913'
appkey = '&appid=' + config.WEATHER_APP_KEY
language = '&lang=kr'


def GetWeatherData():
    url = urllib.request.urlopen(base_url + location + language + appkey)
    api_data = url.read()
    data = json.loads(api_data.decode('utf8'))

    weath_id = data['weather'][0]['id']
    weath_state = data['weather'][0]['description']
    wind_spd = data['wind']['speed']
    temper = round(data['main']['temp'] - 273.15, 2)

    print(weath_id, weath_state, str(wind_spd)+'m/s', str(temper)+'˚C')
    return {'weath_id':weath_id, 'weath_state':weath_state, 'wind_spd':wind_spd, 'temperature' : temper}


@app.route('/', methods = ['GET', 'POST'])
@app.route('/state', methods = ['GET', 'POST'])
def state():
        if request.method == 'GET' :
            sql = "select * from data order by date desc limit 1"
            curs.execute(sql)
            rows = curs.fetchall()
            print(rows)
            return jsonify(rows[0])

        elif request.method == 'POST' :
            data = GetWeatherData()
            # data['water_level'] = 123
            data['water_level'] = request.form['water_level']
            print(data)

            query = 'INSERT INTO data(weather_id, weather_state, wind_speed, water_level, temperature) VALUES (%s, %s, %s, %s, %s)'
            curs.execute(query, (data['weath_id'], data['weath_state'], data['wind_spd'], data['water_level'], data['temperature']))
            conn.commit()

            return jsonify(data)


if __name__== '__main__' :
        app.run(host='0.0.0.0')
        conn.close()
