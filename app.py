import datetime as dt
import numpy as np
import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.Measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def Home():
    """List all available api routes."""
    return(
        f"Hawaii Climate Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"and<br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation/")
def precipitation():
    """Convert the query results to a Dictionary using date as the key and prcp as the value."""
    results = session.query(Measurement.date, Measurement.prcp).\
        group_by(Measurement.date).all()
    
    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    results = session.query(Measurement.stations).\
        group_by(Measurement.stations).all()

    return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
    """query for the dates and temperature observations from a year from the last data point."""
    date = dt.datetime(2017, 8, 23)
    year_ago = date - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= year_ago).\
        filter(Measurement.date <= date).\
        order_by(Measurement.date).all()

    return jsonify(results)


@app.route("/api/v1.0/<start>")
def temp_data(start_date):
    """When given the start only, calculate TMIN, TAVG, and TMAX"""
    """for all dates greater than and equal to the start date."""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def temp_range(start_date, end_date):
    """When given the start and the end date, calculate the TMIN, TAVG, and TMAX"""
    """for dates between the start and end date inclusive."""
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
