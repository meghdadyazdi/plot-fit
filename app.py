import os
from flask import Flask, render_template, redirect, session, request, url_for, jsonify
import json
import pylab as plb
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import scipy.stats as stats

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('fit_gauss.html')

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
    global xdata
    global ydata
    
    xdata = []
    ydata = []
    for d in data:
        if d:
            xdata.append(float(d[0]))
            ydata.append(float(d[1]))
    print(round(xdata[0]-xdata[1], 2))
    print(type(xdata[0]))
    print(xdata)
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    return render_template('fit_gauss.html')

@app.route('/data')
def xydata():
   return jsonify({'xdata': xdata, 'ydata':ydata})

def gauss_fit(peak, area, fwhm):
    xfit = xdata
    yfit = ydata
    n = len(xfit)      
    sigma = float(fwhm) / 2.3548
    amp = float(area) / sigma
    def gaus(x,a,x0,sigma):
        return a*exp(-(x-x0)**2/(2*sigma**2))
    popt,pcov = curve_fit(gaus,xdata,ydata,p0=[amp,float(peak),sigma])
    (amp, peak, sigma) = popt
    yfit = gaus(xfit,*popt).tolist()
    peak_fit = xfit[yfit.index(max(yfit))]
    area_fit = round(max(yfit)*abs(sigma) / 0.3989, 2) # 1/sqrt(2pi)
    height_fit = round(max(yfit), 2)
    fwhm_fit = round(2.3548*abs(sigma), 2) # 2sqrt(2ln2)
    ydiff = [x - y for x, y in zip(ydata, yfit)]
    ydiff2 = [x * 2 for x in ydiff]
    sig = [1]*len(ydiff) #it can be improved
    sig2 = [x * 2 for x in sig]
    chi_square = round(sum([x / y for x, y in zip(ydiff2, sig2)]),2)
    return (xfit, yfit, peak_fit, area_fit, height_fit, fwhm_fit, chi_square)


@app.route('/data_fit')
def data_fit():
    return jsonify({'xfit': xfit,
                    'yfit':yfit,
                    'peak_fit':peak_fit,
                    'area_fit':area_fit,
                    'height_fit':height_fit,
                    'fwhm_fit':fwhm_fit,
                    'chi_square':chi_square})    

if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT', '3000')),
            debug=True)
