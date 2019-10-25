#!/usr/bin/env python
from flask import Flask, url_for, render_template, send_from_directory, request
import jinja2.exceptions
import pickle
import pandas as pd 
import numpy as np 
import sys, os

dir_path = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def read_stock_data(file_name):
    '''
    read and format card stock for the given name
    '''

    with open(os.path.join(dir_path, 'pickles', file_name), 'rb') as handle:
        dfs_concatenated = pickle.load(handle)
    dfs_concatenated_formated = dfs_concatenated.copy().reset_index()
    dfs_concatenated_formated.ts = dfs_concatenated_formated.ts.dt.strftime('%Y-%m-%d %H-%M')
    data_stock = dfs_concatenated_formated.values.tolist()
    return data_stock

schema_stock = [{
  "name": "Time",
  "type": "date",
  "format": "%Y-%m-%d %H-%M" #"%d-%b-%y"
}, {
  "name": "Stock Value",
  "type": "number"
}, {
  "name": "Card Condition",
  "type": "string"
}]

#get card names and strip all non alphabet characters and connect words with '-'
card_names = ['Snow_Covered_Island',
 'Fabled_Passage',
 'Once_Upon_a_Time',
 'Murderous_Rider_Swift_End',
 'Questing_Beast',
 'Oko_Thief_of_Crowns']

@app.route('/')
def index():
    return Snow_Covered_Island()

@app.route('/Snow_Covered_Island')
def Snow_Covered_Island():
    return render_template('Snow_Covered_Island.html', data_stock=read_stock_data('Snow_Covered_Island_stock.pickle'), schema_stock=schema_stock)

@app.route('/Fabled_Passage')
def Fabled_Passage():
    return render_template('Fabled_Passage.html', data_stock=read_stock_data('Fabled_Passage_stock.pickle'), schema_stock=schema_stock)

@app.route('/Once_Upon_a_Time')
def Once_Upon_a_Time():
    return render_template('Once_Upon_a_Time.html', data_stock=read_stock_data('Once_Upon_a_Time_stock.pickle'), schema_stock=schema_stock)

@app.route('/Murderous_Rider_Swift_End')
def Murderous_Rider_Swift_End():
    return render_template('Murderous_Rider_Swift_End.html', data_stock=read_stock_data('Murderous_Rider_Swift_End_stock.pickle'), schema_stock=schema_stock)

@app.route('/Questing_Beast')
def Questing_Beast():
    return render_template('Questing_Beast.html', data_stock=read_stock_data('Questing_Beast_stock.pickle'), schema_stock=schema_stock)


@app.route('/Oko_Thief_of_Crowns')
def Oko_Thief_of_Crowns():
    return render_template('Oko_Thief_of_Crowns.html', data_stock=read_stock_data('Oko_Thief_of_Crowns_stock.pickle'), schema_stock=schema_stock)



#@app.route('/<pagename>')
#def admin(pagename):
#    return render_template(pagename+'.html')

@app.route('/<path:resource>')
def serveStaticResource(resource):
	return send_from_directory('static/', resource)

@app.route('/test')
def test():
    return '<strong>It\'s Alive!</strong>'

@app.errorhandler(jinja2.exceptions.TemplateNotFound)
def template_not_found(e):
    return not_found(e)

@app.errorhandler(404)
def not_found(e):
    return '<strong>Page Not Found!</strong>', 404

if __name__ == '__main__':
    app.run(host= '0.0.0.0')