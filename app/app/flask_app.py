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

'''
read_stock_data
'''
def read_price_distribution_lastest_time_stamp(card_name):
    with open(os.path.join(dir_path, 'pickles', 
        card_name + '_price_distribution_lastest_time_stamp.pickle'), 'rb') as handle:
        data = pickle.load(handle)
    return data

'''
read_item_cheapest_price_item_amount
'''
def read_item_cheapest_price_item_amount(card_name):
    with open(os.path.join(dir_path, 'pickles', 
        card_name + '_item_cheapest_price_item_amount.pickle'), 'rb') as handle:
        data = pickle.load(handle)
    return data

schema_item_cheapest_price_item_amount = [{
  "name": "Time",
  "type": "date",
  "format": "%Y-%m-%d %H-%M" #"%d-%b-%y"
}, {
  "name": "Item Cheapest Price",
  "type": "number"
}, {
  "name": "Stock Value",
  "type": "number"
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
    return render_template('Snow_Covered_Island.html', 
        data_price_distribution_lastest_time_stamp =
            read_price_distribution_lastest_time_stamp('Snow_Covered_Island'), 
        data_item_cheapest_price_item_amount = 
            read_item_cheapest_price_item_amount('Snow_Covered_Island'), 
        schema_item_cheapest_price_item_amount = 
            schema_item_cheapest_price_item_amount)

@app.route('/Fabled_Passage')
def Fabled_Passage():
    return render_template('Fabled_Passage.html', 
        data_price_distribution_lastest_time_stamp =
            read_price_distribution_lastest_time_stamp('Fabled_Passage'), 
        data_item_cheapest_price_item_amount = 
            read_item_cheapest_price_item_amount('Fabled_Passage'), 
        schema_item_cheapest_price_item_amount = 
            schema_item_cheapest_price_item_amount)

@app.route('/Once_Upon_a_Time')
def Once_Upon_a_Time():
    return render_template('Once_Upon_a_Time.html', 
        data_price_distribution_lastest_time_stamp =
            read_price_distribution_lastest_time_stamp('Once_Upon_a_Time'), 
        data_item_cheapest_price_item_amount = 
            read_item_cheapest_price_item_amount('Once_Upon_a_Time'), 
        schema_item_cheapest_price_item_amount = 
            schema_item_cheapest_price_item_amount)

@app.route('/Murderous_Rider_Swift_End')
def Murderous_Rider_Swift_End():
    return render_template('Murderous_Rider_Swift_End.html', 
        data_price_distribution_lastest_time_stamp =
            read_price_distribution_lastest_time_stamp('Murderous_Rider_Swift_End'), 
        data_item_cheapest_price_item_amount = 
            read_item_cheapest_price_item_amount('Murderous_Rider_Swift_End'), 
        schema_item_cheapest_price_item_amount = 
            schema_item_cheapest_price_item_amount)

@app.route('/Questing_Beast')
def Questing_Beast():
    return render_template('Questing_Beast.html', 
        data_price_distribution_lastest_time_stamp =
            read_price_distribution_lastest_time_stamp('Questing_Beast'), 
        data_item_cheapest_price_item_amount = 
            read_item_cheapest_price_item_amount('Questing_Beast'), 
        schema_item_cheapest_price_item_amount = 
            schema_item_cheapest_price_item_amount)


@app.route('/Oko_Thief_of_Crowns')
def Oko_Thief_of_Crowns():
    return render_template('Oko_Thief_of_Crowns.html', 
        data_price_distribution_lastest_time_stamp =
            read_price_distribution_lastest_time_stamp('Oko_Thief_of_Crowns'), 
        data_item_cheapest_price_item_amount = 
            read_item_cheapest_price_item_amount('Oko_Thief_of_Crowns'), 
        schema_item_cheapest_price_item_amount = 
            schema_item_cheapest_price_item_amount)

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