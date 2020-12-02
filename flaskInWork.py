# -*- coding: utf-8 -*-
"""
Created on Mon Nov 23 04:51:31 2020

@author: LENOVO
"""

from flask import Flask,jsonify

app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to machine learning model APIs!"

"""
@app.route("/<string:s>")
def printIt(s):
    J={'key':s}
    return(jsonify(J))"""
    
@app.route("/",methods=['GET','POST'])
def printIt():
    return('Tex')



@app.route("/<int:n>")
def even(n):
    if n%2==0:
        return("Even")
    else:
        return("Odd")

@app.route("/Hi")
def hi():
    return "Hi"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=800,use_reloader=False)