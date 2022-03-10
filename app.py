
from flask import Flask, redirect,render_template,request
from flask.wrappers import Response
import requests
import pickle
import numpy as np
import pandas as pd
import json
from logic import reco ,listt,keys
import random

app=Flask(__name__)
crop_recommendation_model_path = 'models/RandomForest.pkl'
crop_recommendation_model = pickle.load(
    open(crop_recommendation_model_path, 'rb'))
list=[]
def nischay(city):
    data=requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&APPID=bae363c55a4f3c7563608369a789e456")

    data=data.json()
    if data["cod"]!=404:
        data=data["main"]
        list.append(data["temp"])
        list.append(data["humidity"])
        return list
    else:
        return 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/crop-recommender")
def re():
    return render_template("crop-recommender.html")

@app.route("/fertilizer")
def fer():
    return render_template("fertilizer.html")

@app.route('/crop-predict', methods=['POST',"GET"])
def crop_prediction():
    title = 'Agromate - Crop Recommendation'

    if request.method == 'POST':
        N = int(request.form['N'])
        P = int(request.form['P'])
        K = int(request.form['K'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        k=1
        city = request.form.get("city")

        if nischay(city) != 0:
            ivu = nischay(city)
            data = np.array([[N, P, K, ivu[0]-273, ivu[1], ph, rainfall]])
            my_prediction = crop_recommendation_model.predict(data)
            final_prediction = my_prediction[0]

            return render_template("crop-recommender.html", prediction=final_prediction, title=title,k=k)

        else:
            return "<h1 style='width:50%; margin:0 auto 0 auto;'>404</h1>"
        
   

@app.route('/fert-predict', methods=['POST',"GET"])
def fert_prediction():
    N = int(request.form['N'])
    P = int(request.form['P'])
    K = int(request.form['K'])
    if N>41.5:
        return render_template("ivu.html",rem=listt[3],m=keys[3])
    elif N<41.5:
        return render_template("ivu.html",rem=listt[1],m=keys[1])
    elif P>33.25:
        return render_template("ivu.html",rem=listt[5],m=keys[5])
    elif P<33.25:
        return render_template("ivu.html",rem=listt[4],m=keys[4])
    elif K<38.25:
       return render_template("ivu.html",rem=listt[0],m=keys[0])
    elif K>38.25:
        return render_template("ivu.html",rem=listt[2],m=keys[2])
    elif K>50 and P>50 and N>50:
        m=[2,3,5]
        r=random.choice(m)
        return render_template("ivu.html",rem=listt[r],m=keys[r])
    elif K<50 and P<50 and N<50: 
        m=[0,1,4]
        r=random.choice(m)
        return render_template("ivu.html",rem=listt[r],m=keys[r])
    elif K>50 and P>50 and N<50:
        m=[2,5]
        r=random.choice(m)
        return render_template("ivu.html",rem=listt[r],m=keys[r])
    elif K>50 and P<50 and N>50:
        m=[1,4]
        r=random.choice(m)
        return render_template("ivu.html",rem=listt[r],m=keys[r])
    elif K>50 and P<50 and N<50:
        m=[2,4]
        r=random.choice(m)
        return render_template("ivu.html",rem=listt[r],m=keys[r])
    elif K<50 and P>50 and N>50:
        m=[5,3]
        r=random.choice(m)
        return render_template("ivu.html",rem=listt[r],m=keys[r])
    elif K<50 and P>50 and N<50:
        m=[0,2]
        r=random.choice(m)
        return render_template("ivu.html",rem=listt[r],m=keys[r])
    elif K<50 and P<50 and N>50:
        m=[0,4]
        r=random.choice(m)
        return render_template("ivu.html",rem=listt[r],m=keys[r])
    elif K<50 and P<50 and N<50: 
         m=[0,2,4]
         r=random.choice(m)
         return render_template("ivu.html",rem=listt[r],m=keys[r])
    else:
        m=[0,1,2,3,4,5]
        r=random.choice(m)
        return render_template("ivu.html",rem=listt[r],m=keys[r])


        
if __name__=="__main__":
    app.run()
