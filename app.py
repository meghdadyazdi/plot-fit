import os
from flask import Flask, render_template, redirect, session, request, url_for, jsonify
# from flask_pymongo import PyMongo
# from bson.objectid import ObjectId
# import bcrypt
# import re
# from datetime import date
from bson import Binary, Code, json_util
from bson.json_util import dumps, loads
import json
# from os import path
# if path.exists("env.py"):
#   import env

# import matplotlib.pyplot as plt
# import numpy as np


# import glob
# os.chdir("/workspace/cookbook/data/plot")
# for file in glob.glob("*.txt"):
#     print(file)



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('fit_gauss.html')




# @app.route('/data')
@app.route('/', methods=['POST','GET'])
def upload_and_fit():
    if request.form.get('peak'):
        peak = request.form.get('peak')
        area = request.form.get('area')
        fwhm = request.form.get('fwhm')
        global xfit
        global yfit
        global peak_fit
        global area_fit
        global height_fit
        global fwhm_fit
        global chi_square
        (xfit, yfit, peak_fit, area_fit, height_fit, fwhm_fit, chi_square) = gauss_fit(peak, area, fwhm)
        return render_template('fit_gauss.html')
    uploaded_file = request.files['file']
    print("----",uploaded_file.filename)
    for line in uploaded_file:
        if line.decode("utf-8").startswith('[Data'):
            break
    # Read the rest of the data, using spaces to split. 
    data = [r.decode("utf-8").split() for r in uploaded_file]
    # xdata = data[:,0]
    # ydata = data[:,1]
    global xdata
    global ydata
    
    xdata = []
    ydata = []
    print("------------------------------")
    for d in data:
        if d:
            xdata.append(float(d[0]))
            ydata.append(float(d[1]))
    print(round(xdata[0]-xdata[1], 2))
    # print(ydata)
    print(type(xdata[0]))
    print(xdata)
    # print(type(ydata))
    # print(ydata)
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    
    # global dataxy
    # dataxy = jsonify({'xdata': xdata, 'ydata':ydata})
    return render_template('fit_gauss.html')
    # return render_template('fit_gauss.html', data=jsonify({'xdata': xdata, 'ydata':ydata}))
    # return render_template("fit_gauss.html")

@app.route('/data')
def xydata():
   return jsonify({'xdata': xdata, 'ydata':ydata})

@app.route('/data_fit')
def data_fit():
    return jsonify({'xfit': xfit,
                    'yfit':yfit,
                    'peak_fit':peak_fit,
                    'area_fit':area_fit,
                    'height_fit':height_fit,
                    'fwhm_fit':fwhm_fit,
                    'chi_square':chi_square})


def gauss_fit(peak, area, fwhm):
    print('!!!!!!!!!!!------1111',xdata)
    xfit = xdata
    yfit = [y+.6 for y in ydata]
    print('+++yfit++++', yfit)
    print('+++xfit++++', xfit)
    print('+++peak++++', peak)
    # print('+++peak_fit++++', type(peak_fit))
    
    peak_fit = float(peak) + 2
    area_fit = float(area) + 2
    height_fit = 7.5
    fwhm_fit = float(fwhm) + 2
    chi_square = .2
    
    return (xfit, yfit, peak_fit, area_fit, height_fit, fwhm_fit, chi_square)

    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '5556')),
            debug=True)
