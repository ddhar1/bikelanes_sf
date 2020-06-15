# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 11:46:07 2019

@author: Divya
"""

import json
from flask import Flask, render_template, url_for
import pandas as pd
import numpy as np
import os

# import the file which has accidents and the bike lane and raod it was on
accidents_bikelane_road = pd.read_csv( 'BikewayNetwork_edit\\accidents_bikelanes_roads_wlengths.csv', engine='python')
# alternative way of importing data: os.path.join('C:', 'Users', 'name')

year_names = np.unique(accidents_bikelane_road['accident_year']).tolist()

def calc_standard( row ):
    ''' 
    calc_standard standardizes the number accidents metric by road length 
    '''
    if row['bikelane_exist'] == "No":
        return (row['accident_counts']/row['road_length'] )
    else:
        return (row['accident_counts'] /row['bikelane_length_haver'])

def isWeekday( x ):
    ''' 
    Creates an indicator for whether or not the day of the week in the column is a weekday
    '''
    if x in ( 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ) :
        return('Weekday')
    else: # assuming no errors in our dataset, oc
        return('Weekend')

# Not applying isWeekday to the accident dataset in the mean time - will be used for a future graph    
#accidents_bikelane_road['isWeekday'] = accidents_bikelane_road.DayOfWeek.apply( lambda x: isWeekday( x))

# Data Manipulations to get a graph that shows standardized number of accidents by year, for a SF District
accident_counts_bydistrict_bikelane_exist = accidents_bikelane_road.groupby(['bikelane_exist', 'PdDistrict', 'accident_year', 'cnn_of_road', 'globalid', 'road_length', 'bikelane_length_haver']).agg({'Category':'count'}).reset_index()
accident_counts_bydistrict_bikelane_exist.rename( columns = {'Category': 'accident_counts'}, inplace = True)
accident_counts_bydistrict_bikelane_exist = accident_counts_bydistrict_bikelane_exist.groupby( ['bikelane_exist', 'PdDistrict', 'accident_year'], as_index = False)['accident_counts','road_length', 'bikelane_length_haver'].sum()
accident_counts_bydistrict_bikelane_exist['std_metric'] = accident_counts_bydistrict_bikelane_exist.apply(calc_standard, axis = 1)
    
accident_counts_bydistrict_bikelane_exist = accident_counts_bydistrict_bikelane_exist.drop( ['accident_counts',
       'road_length', 'bikelane_length_haver'], axis = 1)


# Start a new flask app
app = Flask(__name__, static_url_path='/static') 
# where static_url_path is location of static files such as d3, .css

# prevent browser caching
# https://stackoverflow.com/questions/21714653/flask-css-not-updating
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)
def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

# Flask will send returned information to main page of the app
@app.route('/')
@app.route('/index.html') # ties route to upcoming def to front page of website
def index():

    # In order to have one color for accident counts on a bike lane, and another graph color for accident counts
    # off a bike lane, I seperate the dataframe into two groups. One on a bikelane, and one off.
    accident_counts_bydistrict_yesbikelane = accident_counts_bydistrict_bikelane_exist.loc[accident_counts_bydistrict_bikelane_exist.bikelane_exist == True, ]
    accident_counts_bydistrict_yesbikelane = accident_counts_bydistrict_yesbikelane.drop('bikelane_exist', axis = 1)
    
    # converts dataframe to dictionary, which is then converted to json
    accident_counts_bydistrict_yesbikelane_dict = accident_counts_bydistrict_yesbikelane.to_dict(orient='records')
    accident_counts_bydistrict_yesbikelane_json = json.dumps(accident_counts_bydistrict_yesbikelane_dict, indent=2)
    accident_counts_bydistrict_yesbikelane_json = {'accident_counts_bydistrict_yesbikelane_json': accident_counts_bydistrict_yesbikelane_json}
    
    # List of unique districts that we'll use to create drop down in javascript
    districts = np.unique(accident_counts_bydistrict_yesbikelane.PdDistrict)

    accident_counts_bydistrict_nobikelane = accident_counts_bydistrict_bikelane_exist.loc[accident_counts_bydistrict_bikelane_exist.bikelane_exist == False, ]
    accident_counts_bydistrict_nobikelane = accident_counts_bydistrict_nobikelane.drop('bikelane_exist', axis = 1)

    accident_counts_bydistrict_nobikelane_dict = accident_counts_bydistrict_nobikelane.to_dict(orient='records')
    accident_counts_bydistrict_nobikelane_json = json.dumps(accident_counts_bydistrict_nobikelane_dict, indent=2)
    accident_counts_bydistrict_nobikelane_json = {'accident_counts_bydistrict_nobikelane_json': accident_counts_bydistrict_nobikelane_json}

    #return render_template("index.html", yesbikelane=accident_counts_bydistrict_yesbikelane_json,
                           #nobikelane = accident_counts_bydistrict_nobikelane_json) 
    
  
    return render_template("index.html", accident_counts_bydistrict_yesbikelane_json=accident_counts_bydistrict_yesbikelane_json,  accident_counts_bydistrict_nobikelane_json=accident_counts_bydistrict_nobikelane_json, districts=districts  )


# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True) # runs on port 5000 and debug is true (not sure what extent is debugged!)
    # automatically renders code changes without you doing any work