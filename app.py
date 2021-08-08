from flask import Flask
app = Flask(__name__)
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite", connect_args={"check_same_thread": False})

# code to reflect the database
Base = automap_base()

# code to reflect to reflect the tables database
Base.prepare(engine, reflect=True)

# create a variable for each of the classes so that we can reference them
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database
session = Session(engine)

# create a Flask application called "app."
@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')


    # Precipitation Route
#defining the route and route name. 
@app.route("/api/v1.0/precipitation")

#create a new function called precipitation()
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return precip

# Stations Route
 #defining the route and route name. 
@app.route("/api/v1.0/stations")

#create a new function called stations()
def stations():
    
    # a query that will allow us to get all of the stations in our database
    results = session.query(Station.station).all()
    
    # start by unraveling our results into a one-dimensional array
    # with results as our parameter, convert the results to a list
    stations = list(np.ravel(results))
    
    # to return our list as JSON, we need to add stations=stations, http://localhost:5000/
    return jsonify(stations=stations)

    # Monthly Temperature Route
# defining the route with this code
@app.route("/api/v1.0/tobs")

# create a function called temp_monthly()
def temp_monthly():
    # calculate the date one year ago from the last date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    # query the primary station for all the temperature observations from the previous year
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    
    # unravel the results into a one-dimensional array,convert that array into a list then jsonify the list and return our results
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

    # Statistics Route - to see the minimum, maximum, and average temperatures
# defining the route with this code, a starting and ending date
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

# create a function called stats()
def stats(start=None, end=None):
    # create a query to select the minimum, average, and maximum temp, a list called sel,asterisk is used to indicate there will be multiple results for our query: minimum, average, and maximum temperatures
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    # determine the starting and ending date,by if-not,unravel the results into a one-dimensional array,convert to a list, jsonify our results, return them.
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)
    
    # use sel list to calculate the min,max,avg,and dates
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

# Initiate funct
if __name__ == "__main__":
    app.run(debug=True)   