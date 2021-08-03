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
engine = create_engine("sqlite:///hawaii.sqlite")

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
app = Flask(__name__)
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
    