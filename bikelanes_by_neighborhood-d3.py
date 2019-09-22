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
accidents_bikelane_road = pd.read_csv(r'C:\Users\Divya\Google Drive\bike-lane-code4sf\BikewayNetwork_edit\accidents_bikelanes_roads_wlengths.csv', engine='python')
# alternative way of importing data: os.path.join('C:', 'Users', 'name')

year_names = np.unique(accidents_bikelane_road['accident_year']).tolist()

def calc_standard( row ):
    if row['bikelane_exist'] == "No":
        return (row['traffic_accidents']/row['road_length'] )
    else:
        return (row['traffic_accidents'] /row['bikelane_length_haver'])
    
def isWeekday( x ):
    if x in ( 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday' ):
        return('Weekday')
    else: # assuming no errors in our dataset, oc
        return('Weekend')
        
#accidents_bikelane_road['isWeekday'] = accidents_bikelane_road.DayOfWeek.apply( lambda x: isWeekday( x))

def calc_standard( row ):
    """ Standardizes accidents measure by 
        length of road with and without a bike lane
    """
    if row['bikelane_exist'] == "No":
        return (row['accident_counts']/row['road_length'] )
    else:
        return (row['accident_counts'] /row['bikelane_length_haver'])

accident_counts_bydistrict_bikelane_exist = accidents_bikelane_road.groupby(['bikelane_exist', 'PdDistrict', 'accident_year', 'cnn_of_road', 'globalid', 'road_length', 'bikelane_length_haver']).agg({'Category':'count'}).reset_index()
accident_counts_bydistrict_bikelane_exist.rename( columns = {'Category': 'accident_counts'}, inplace = True)
accident_counts_bydistrict_bikelane_exist = accident_counts_bydistrict_bikelane_exist.groupby( ['bikelane_exist', 'PdDistrict', 'accident_year'], as_index = False)['accident_counts','road_length', 'bikelane_length_haver'].sum()
accident_counts_bydistrict_bikelane_exist['std_metric'] = accident_counts_bydistrict_bikelane_exist.apply(calc_standard, axis = 1)
    
accident_counts_bydistrict_bikelane_exist = accident_counts_bydistrict_bikelane_exist.drop( ['accident_counts',
       'road_length', 'bikelane_length_haver'], axis = 1)

# Start a new flask app
app = Flask(__name__, static_url_path='/static') # where static_url_path is location of static files such as d3, .css

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


@app.route('/')
@app.route('/index.html') # ties route to upcoming def to front page of website
def index():
    # Determine the selected feature
    #current_feature_name = request.args.get("feature_name")
    #if current_feature_name == None:
    #    current_feature_name = 2003
    #plot2 = create_figure( current_feature_name ) # returns a temporary image file


## accident_counts_bydistrict_yesbikelane
    accident_counts_bydistrict_yesbikelane = accident_counts_bydistrict_bikelane_exist.loc[accident_counts_bydistrict_bikelane_exist.bikelane_exist == True, ]
    accident_counts_bydistrict_yesbikelane = accident_counts_bydistrict_yesbikelane.drop('bikelane_exist', axis = 1)

    accident_counts_bydistrict_yesbikelane_dict = accident_counts_bydistrict_yesbikelane.to_dict(orient='records')
    accident_counts_bydistrict_yesbikelane_json = json.dumps(accident_counts_bydistrict_yesbikelane_dict, indent=2)
    accident_counts_bydistrict_yesbikelane_json = {'accident_counts_bydistrict_yesbikelane_json': accident_counts_bydistrict_yesbikelane_json}

    districts = np.unique(accident_counts_bydistrict_yesbikelane.PdDistrict)
    #accident_counts_bydistrict_nobikelane = accident_counts_bydistrict_bikelane_exist.loc[accident_counts_bydistrict_bikelane_exist.bikelane_exist == False, ]
    #accident_counts_bydistrict_nobikelane = accident_counts_bydistrict_nobikelane.drop('bikelane_exist', axis = 1)
    #accident_counts_bydistrict_nobikelane_dict = accident_counts_bydistrict_nobikelane.to_dict(orient='records')
    #accident_counts_bydistrict_nobikelane_json = json.dumps(accident_counts_bydistrict_nobikelane_dict, indent=2)
    #accident_counts_bydistrict_nobikelane_json = {'chart_data': accident_counts_bydistrict_nobikelane_json}

    #return render_template("index.html", yesbikelane=accident_counts_bydistrict_yesbikelane_json,
                           #nobikelane = accident_counts_bydistrict_nobikelane_json) 
    
    
    # converts dataframe to dictionary, which is then converted to json
    # maybe consider 
    #df = pd.DataFrame( [{ "name": "Original Word Count","wc": 100},{"name": "Model Word Count","wc": 90}] )
    #chart_data = df.to_dict(orient='records')
    #chart_data = json.dumps(chart_data, indent=2) # changes dictionary to json formatted string, which we 
    #data = {'chart_data': chart_data} # dictionary we'll send to web browswer
    return render_template("index.html", accident_counts_bydistrict_yesbikelane_json=accident_counts_bydistrict_yesbikelane_json, \
                           districts=districts  )

	# Embed plot into HTML via Flask Render
	#script, div = components(plot)
   # render template takes the page url that renders this flask app, as well as 

#@app.route('/data1.json')
#def get_d3_data():
#    df = pd.DataFrame([ { "name": "Original Word Count","wc": 100},{"name": "Model Word Count","wc": 90}])
    
    #chart_data = test_data.to_dict(orient='records')
    
    # Constructed however you need it
#    return df.to_json(orient="records")

# if you want more pages, you would declare other def such as def contact, home, etc!
# unsure at this point if there are args in the index page
# delete these comments about flask apps later! not v professional tbh

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True) # runs on port 5000 and debug is true (not sure what extent is debugged!)
    # automatically renders code changes without you doing any work