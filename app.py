from flask import Flask, render_template, url_for, request, redirect
import numpy as np
import requests
from flask_cors import cross_origin
import sklearn
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)
model = pickle.load(open("model.pkl","rb"))

@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")

@app.route('/predict',methods = ['POST','Get'])
@cross_origin()
def job():
	
	if request.method == "POST":
		
		Date, Month, Arrival_hour, Arrival_min, dep_hour, dep_min = 0 ,0 ,0,0,0,0
		Duration_hours, Duration_mins, Stops = 0, 0 ,0
		Air_Asia, Air_India,GoAir, IndiGo, Jet_Airways = 0 , 0 , 0 ,0 ,0
		Jet_Airways_Business ,Multiple_carriers, Multiple_carriers_Premium_economy, SpiceJet = 0,0,0,0
		Trujet, Vistara, Vistara_Premium_economy = 0,0,0
		s_Banglore, s_Chennai,s_Delhi, s_Kolkata, s_Mumbai = 0, 0, 0, 0, 0
		d_Banglore, d_Cochin, d_Delhi,d_Hyderabad, d_Kolkata, d_New_Delhi = 0 ,0, 0 ,0 ,0 ,0
		
		dep_time = request.form['Dep_Time']
		Date = int(pd.to_datetime(dep_time,format="%Y-%m-%dT%H:%M").day)
		Month = int(pd.to_datetime(dep_time,format="%Y-%m-%dT%H:%M").month)
		dep_hour = int(pd.to_datetime(dep_time, format ="%Y-%m-%dT%H:%M").hour)
		dep_min = int(pd.to_datetime(dep_time,format = "%Y-%m-%dT%H:%M").minute)
		
		arr_time = request.form['Arrival_Time']
		Arrival_hour = int(pd.to_datetime(dep_time, format ="%Y-%m-%dT%H:%M").hour)
		Arrival_min = int(pd.to_datetime(dep_time, format ="%Y-%m-%dT%H:%M").minute)

		Duration_hours = abs(Arrival_hour - dep_hour) 
		Duration_mins = abs(Arrival_min - dep_min) 

		source = request.form['Source']
		
		if source == 'Banglore':
			s_Banglore =1
		elif source == 'Chennai':
			s_Chennai = 1
		elif source == 'Delhi':
			s_Delhi = 1
		elif source == 'Kolkata' :
			s_Kolkata = 1
		elif source == 'Mumbai':
			s_Mumbai = 1


		dest = request.form['Destination']
		if dest == 'Banglore':
			d_Banglore =1
		elif dest == 'Cochin':
			d_Cochin = 1
		elif dest == 'Delhi':
			d_Delhi = 1
		elif dest == 'New Delhi':
			d_New_Delhi = 1
		elif dest == 'Kolkata' :
			d_Kolkata = 1
		elif source == 'd_Hyderabad':
			d_Hyderabad = 1

		stops = request.form['stops']
		Stops = int(stops)

		airline = request.form['airline']
		airlines =  [Air_Asia, Air_India,GoAir, IndiGo, Jet_Airways, Jet_Airways_Business,Multiple_carriers, Multiple_carriers_Premium_economy, SpiceJet,Trujet, Vistara, Vistara_Premium_economy]
		airline_list = [0 for i in range(len(airlines))]
		index =0 
		for i,j in enumerate(airlines) :
			if i == airline:
				index = j
				break
		airline_list[index] = 1

		dates_list = [Date, Month, Arrival_hour, Arrival_min, dep_hour, dep_min,Duration_hours, Duration_mins, Stops]
		locs_list = [ s_Banglore, s_Chennai,s_Delhi, s_Kolkata, s_Mumbai, d_Banglore, d_Cochin, d_Delhi,d_Hyderabad, d_Kolkata, d_New_Delhi]
		data =  dates_list + airline_list + locs_list

		y_pred = model.predict([data])

		return render_template('home.html',context ="Your flight price will be ruppees {}".format( round(y_pred[0],2)))
	return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)