import json
import pickle
import pandas as pd
from flask import Flask, request, jsonify


model = pickle.load(open("flight_rf.pkl", "rb"))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def query_records():
    # return jsonify({'error': 'data not found'})
    return 'this is home  page'







@app.route('/predict', methods=['POST'])
def predict():
    output = 0
    record = json.loads(request.data)
     # Date_of_Journey
    date_dep = record["Dep_Time"]
    Journey_day = int(pd.to_datetime(date_dep, format="%Y/%m/%d %H:%M").day)
    Journey_month = int(pd.to_datetime(date_dep, format ="%Y/%m/%d %H:%M").month)
    # print("Journey Date : ",Journey_day, Journey_month)

    # Departure
    Dep_hour = int(pd.to_datetime(date_dep, format ="%Y/%m/%d %H:%M").hour)
    Dep_min = int(pd.to_datetime(date_dep, format ="%Y/%m/%d %H:%M").minute)
    # print("Departure : ",Dep_hour, Dep_min)

    # Arrival
    date_arr = record["Arrival_Time"]
    Arrival_hour = int(pd.to_datetime(date_arr, format ="%Y/%m/%d %H:%M").hour)
    Arrival_min = int(pd.to_datetime(date_arr, format ="%Y/%m/%d %H:%M").minute)
    # print("Arrival : ", Arrival_hour, Arrival_min)

    # Duration  
    dur_hour = abs(Arrival_hour - Dep_hour)
    dur_min = abs(Arrival_min - Dep_min)
    # print("Duration : ", dur_hour, dur_min)

    # Total Stops
    Total_stops = int(record["stops"])
    # print(Total_stops)

    # Airline
    # AIR ASIA = 0 (not in column)
    airline= record['airline']
    flights = {
        "Jet_Airways" : 0,
        "IndiGo" : 0,
        "Air_India" : 0,
        "Multiple_carriers" : 0,
        "SpiceJet" : 0,
        "Vistara" : 0,
        "GoAir" : 0,
        "Multiple_carriers_Premium_economy" : 0,
        "Jet_Airways_Business": 0,
        "Vistara_Premium_economy" : 0,
        "Trujet" : 0
            }
    flights[airline] = 1

    Source = record["Source"]
    so_city = {
        "s_Delhi" : 0,
        "s_Kolkata" : 0,
        "s_Mumbai" : 0,
        "s_Chennai" : 0
    }
    so_city[Source] = 1
    
    
    Destination = record["Destination"]
    de_city={
        "d_Cochin" :0,
        "d_Delhi" : 0,
        "d_New_Delhi" : 0,
        "d_Hyderabad" : 0,
        "d_Kolkata" : 0
        }
    de_city[Destination] = 1

    prediction=model.predict([[
        Total_stops,
        Journey_day,
        Journey_month,
        Dep_hour,
        Dep_min,
        Arrival_hour,
        Arrival_min,
        dur_hour,
        dur_min,
        flights["Air_India"],
        flights["GoAir"],
        flights["IndiGo"],
        flights["Jet_Airways"],
        flights["Jet_Airways_Business"],
        flights["Multiple_carriers"],
        flights["Multiple_carriers_Premium_economy"],
        flights["SpiceJet"],
        flights["Trujet"],
        flights["Vistara"],
        flights["Vistara_Premium_economy"],
        so_city["s_Chennai"],
        so_city["s_Delhi"],
        so_city["s_Kolkata"],
        so_city["s_Mumbai"],
        de_city["d_Cochin"],
        de_city["d_Delhi"],
        de_city["d_Hyderabad"],
        de_city["d_Kolkata"],
        de_city["d_New_Delhi"]
    ]])

    output=round(prediction[0],2)+2700

    print(record)
    print(output)

    return jsonify({'output': output})
app.run(debug=True)