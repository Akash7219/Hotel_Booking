from flask import Flask,request,render_template
import joblib
import numpy as np
import sklearn
import pickle
import pandas as pd

filename="randomm.pkl"
model=joblib.load(open(filename,'rb'))

app=Flask(__name__)


@app.route("/")
def home():
    return render_template("result.html")

@app.route("/predict",methods=["GET","POST"])
def predict():
    with_family_or_else=0
    booking_changes=0
    days_in_waiting=0
    if request.method=="POST":
        hotel=request.form["hotel"]
        lead_time=int(request.form["lead_time"])
        month=int(request.form["month"])
        meal=int(request.form["meal"])
        market_seg=int(request.form["market_segment"])
        distribution=int(request.form["distribution_channel"])
        deposit=int(request.form["deposit_type"])
        customer=int(request.form["customer_type"])
        repeated_guest=int(request.form["repeated_guest"])
        car_park=int(request.form["car_parking"])
        special_req=int(request.form["special_requests"])
        diff_room=int(request.form["diff_room_assigned"])
        adr=float(request.form["adr"])
        weekend_night=int(request.form["stays_in_weekend_night"])
        week_night=int(request.form["stays_in_week_nights"])
        if week_night<4:
            week_nights_stay=0
        elif week_night>3 and week_night<9:
            week_nights_stay=2
        elif week_night>8:
            week_nights_stay=1
        total_night_stayed=weekend_night+week_night
        adult=int(request.form["adults"])
        children=int(request.form["children"])
        babies=int(request.form["babies"])
        if adult==1 and (children==0 and babies==0):
            with_family_or_else=2
        elif adult>0 and (children>0 or babies>0):
            with_family_or_else=4
        elif adult<3 and (children==0 and babies==0):
            with_family_or_else=3
        elif 3<=adult<=6 and (children==0 and babies==0):
            with_family_or_else=1
        elif adult>6 and (children==0 and babies==0):
            with_family_or_else=0
        booking_changes=int(request.form["no_of_booking_changes"])
        if booking_changes==0:
            booking_changes_made=2
        elif 0<booking_changes<5:
            booking_changes_made=0
        else:
            booking_changes_made=1
        waiting_days=int(request.form["days_in_waiting_list"])
        if waiting_days<7:
            days_in_waiting=0
        elif 6<waiting_days<30:
            days_in_waiting=2
        else:
            days_in_waiting=1
        prediction_list=[hotel,
                        lead_time,
                        month,
                        meal,
                        market_seg,
                        distribution,
                        repeated_guest,
                        deposit,
                        customer, 
                        adr, 
                        car_park,
                        special_req, 
                        total_night_stayed,
                        with_family_or_else, 
                        diff_room, 
                        week_nights_stay,
                        booking_changes_made,
                        days_in_waiting]
        predict_array=np.array([prediction_list])
        prediction_model=model.predict(predict_array)
        output=prediction_model[0]
        if int(output)== 1: 
            predictor ='The customer will cancel the booking'
        else: 
            predictor ='The customer will not cancel the booking'            
        return render_template("result.html", prediction = predictor)
    else:
        return render_template("result.html")
if __name__=="__main__":
    app.run(debug=True)

        

        
    
