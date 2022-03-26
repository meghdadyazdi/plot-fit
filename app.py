import os
from flask import Flask, render_template, redirect, session, request, url_for, jsonify
import json


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('fit_gauss.html')



@app.route('/', methods=['POST','GET'])
def upload_and_fit():
    uploaded_file = request.files['file']
    print("----",uploaded_file.filename)
    for line in uploaded_file:
        if line.decode("utf-8").startswith('[Data'):
            break
    # Data 
    data = [r.decode("utf-8").split() for r in uploaded_file]
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
    return render_template('fit_gauss.html')

if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '3000')),
            debug=True)
