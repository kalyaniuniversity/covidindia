# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 11:37:28 2020

@author: Dripta
"""

from flask import Flask, jsonify, request, render_template, url_for
from ..covidindia import *
from flask import Response
import json
from datetime import datetime, timedelta
import numpy as np

init = initializer(silent=True)
filter_data = Data(init)
demo = Demographic_overview(init, silent=True)
plot = visualizer(init)
app = Flask(__name__, static_url_path='/public')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template('index_home.html')
    elif request.method == 'POST':

        value = request.form['result_data']
        df = init.show_data(of=value.split(' ')[1].replace('"', ''))
        df = df.to_json(orient='records')
        return df


@app.route('/State', methods=['GET', 'POST'])
def state():
    if request.method == 'GET':
        return render_template('index_state.html')
    elif request.method == 'POST':
        state_name = request.form['state_data'].replace('"', '')
        daily = request.form['daily_data'].replace('"', '')
        try:
            condition = request.form['condition_data'].replace('"', '')
        except:
            pass
        if state_name == 'All':
            if daily == 'Yes':
                df = filter_data.get_dataset_state(state='Whole', daily=True)
                return df[condition].to_json(orient='records')
            else:
                df = filter_data.get_dataset_state(state='Whole', daily=False)
                df = df.to_json(orient='records')
                return df
        else:
            if daily == 'Yes':
                df = filter_data.get_dataset_state(
                    state=state_name, daily=True).reset_index()
                df.columns = ['Date', 'Confirmed', 'Recovered', 'Death']
                df = df.to_json(orient='records')

                return df
            else:
                df = filter_data.get_dataset_state(
                    state=state_name, daily=False)
                df = df.to_json(orient='records')
                return df


@app.route('/Demography', methods=['GET', 'POST'])
def demography():
    if request.method == 'GET':
        return render_template('index_demo.html')
    elif request.method == 'POST':
        place = request.form['place_data']
        date = request.form['date_day']
        try:
            df = demo.demography(place=place.lower(),
                                 date=date.lower()).reset_index()
            for i, j in enumerate(df.dateannounced):
                df.dateannounced[i] = datetime.strftime(j, '%d/%m/%Y')

            df = df.to_json(orient='records')
            return Response(df,  mimetype='application/json')
        except:
            return 'None'


@app.route('/filter', methods=['POST'])
def disfilter():
    place_name = request.form['place_data']
    df = demo.raw[demo.raw['detectedstate'] == place_name]
    if df.empty == False:
        result_list = list(np.unique([i for i in df['detecteddistrict']]))
        return Response(json.dumps(result_list),  mimetype='application/json')
    else:
        df = demo.raw[demo.raw['detecteddistrict'] == place_name]
        result_list = list(np.unique([i for i in df['detectedcity']]))
        return Response(json.dumps(result_list),  mimetype='application/json')


@app.route('/Rank', methods=['GET', 'POST'])
def rank():
    if request.method == 'GET':
        return render_template('index_rank.html')
    elif request.method == 'POST':
        kind = request.form['kind_data']
        num = int(request.form['number_data'])
        by = request.form['by_data']
        cumulative = request.form['cumulative_data']
        date = request.form['date_data']
        if date == 'None':
            if cumulative == 'False':
                state = request.form['state_data']
                df = filter_data.rank(
                    num=num, by=by, kind=kind.lower(), cumulative=False)
                df = pd.DataFrame(df[state]).reset_index()
                df.columns = ['Date', f'{state}']
                df = df.to_json(orient='records')
                return Response(df,  mimetype='application/json')
            else:
                df = filter_data.rank(
                    num=num, by=by, kind=kind.lower(), cumulative=True)
                df = df.to_json(orient='records')
                return Response(df,  mimetype='application/json')

        else:
            if cumulative == 'False':
                df = filter_data.rank(
                    num=num, by=by, kind=kind.lower(), cumulative=False, date=date)
                df = df.to_json(orient='records')
                return Response(df,  mimetype='application/json')
            else:
                df = filter_data.rank(
                    num=num, by=by, kind=kind.lower(), cumulative=True, date=date)
                df = df.to_json(orient='records')
                return Response(df,  mimetype='application/json')


@app.route('/Graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'GET':
        return render_template('index_graph.html')
    elif request.method == 'POST':
        state_name = request.form['state_data'].replace('"', '')
        daily = request.form['daily_data'].replace('"', '')
        condition = request.form['condition_data'].replace('"', '')
        if state_name == 'All':
            if daily == 'Yes':
                if condition == 'Confirmed':
                    df = init.count_conf
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                elif condition == 'Recovered':
                    df = init.count_recover
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                elif condition == 'Deceased':
                    df = init.count_death
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                elif condition == 'Together':
                    df_1 = init.count_conf.to_json(orient='records')
                    df_2 = init.count_recover.to_json(orient='records')
                    df_3 = init.count_death.to_json(orient='records')
                    df_list = [df_1, df_2, df_3]
                    return Response(json.dumps(df_list),  mimetype='application/json')
            else:
                if condition == 'Confirmed':
                    df = init.csv_Confirmed
                    df = df.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR)', 'LONGITUDE',
                                          'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                elif condition == 'Recovered':
                    df = init.csv_recovered
                    df = df.drop(columns=['POPULATION', 'LONGITUDE', 'PER CAPITA INCOME (INR) ',
                                          'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                elif condition == 'Deceased':
                    df = init.csv_Death
                    df = df.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR) ', 'LONGITUDE',
                                          'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                elif condition == 'Together':
                    df_1 = init.csv_Confirmed.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR)', 'LONGITUDE',
                                                            'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                    df_1 = df_1.to_json(orient='records')
                    df_2 = init.csv_recovered.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR) ', 'LONGITUDE',
                                                            'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                    df_2 = df_2.to_json(orient='records')
                    df_3 = init.csv_Death.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR) ', 'LONGITUDE',
                                                        'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                    df_3 = df_3.to_json(orient='records')
                    df_list = [df_1, df_2, df_3]
                    return Response(json.dumps(df_list),  mimetype='application/json')
        else:
            if daily == 'Yes':
                if condition == 'Confirmed':
                    df = init.count_conf[init.count_conf['STATE/UT']
                                         == state_name]
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                elif condition == 'Recovered':
                    df = init.count_recover[init.count_recover['STATE/UT']
                                            == state_name]
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                elif condition == 'Deceased':
                    df = init.count_death[init.count_death['STATE/UT']
                                          == state_name]
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                elif condition == 'Together':
                    df_1 = init.count_conf[init.count_conf['STATE/UT']
                                           == state_name].to_json(orient='records')
                    df_2 = init.count_recover[init.count_recover['STATE/UT']
                                              == state_name].to_json(orient='records')
                    df_3 = init.count_death[init.count_death['STATE/UT']
                                            == state_name].to_json(orient='records')
                    df_list = [df_1, df_2, df_3]
                    return Response(json.dumps(df_list),  mimetype='application/json')
            else:
                if condition == 'Confirmed':
                    df = init.csv_Confirmed[init.csv_Confirmed['STATE/UT']
                                            == state_name]
                    df = df.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR)', 'LONGITUDE',
                                          'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                elif condition == 'Recovered':
                    df = init.csv_recovered[init.csv_recovered['STATE/UT']
                                            == state_name]
                    df = df.drop(columns=['POPULATION', 'LONGITUDE', 'PER CAPITA INCOME (INR) ',
                                          'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                elif condition == 'Deceased':
                    df = init.csv_Death[init.csv_Death['STATE/UT']
                                        == state_name]
                    df = df.drop(columns=['POPULATION', 'PER CAPITA INCOME (INR) ', 'LONGITUDE',
                                          'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                    df = df.to_json(orient='records')
                    return Response(df,  mimetype='application/json')
                elif condition == 'Together':
                    df_1 = init.csv_Confirmed[init.csv_Confirmed['STATE/UT'] == state_name].drop(columns=['POPULATION', 'PER CAPITA INCOME (INR)', 'LONGITUDE',
                                                                                                          'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                    df_1 = df_1.to_json(orient='records')
                    df_2 = init.csv_recovered[init.csv_recovered['STATE/UT'] == state_name].drop(columns=['POPULATION', 'PER CAPITA INCOME (INR) ', 'LONGITUDE',
                                                                                                          'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                    df_2 = df_2.to_json(orient='records')
                    df_3 = init.csv_Death[init.csv_Death['STATE/UT'] == state_name].drop(columns=['POPULATION', 'PER CAPITA INCOME (INR) ', 'LONGITUDE',
                                                                                                  'LATITUDE', 'CODE', 'AVERAGE TEMPERATURE (°C)'])
                    df_3 = df_3.to_json(orient='records')
                    df_list = [df_1, df_2, df_3]
                    return Response(json.dumps(df_list),  mimetype='application/json')


if __name__ == 'covdata.SERVER.server':
    app.run(debug=True, use_reloader=True)
