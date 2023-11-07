from core import app
from flask import Flask, render_template

import oracledb

currentQuery = 1

connection = oracledb.connect(user="obisset", password="B69SI5SeQAugPl6lHcd5YrL4", dsn="oracle.cise.ufl.edu:1521/orcl")


cursor = connection.cursor()

@app.route('/')
def index():
    return 'Hello Ace123'


@app.route('/home')
def about():
    return render_template('index.html', headline="Hello World!")

# querySelector

@app.route('/querySelector')
def querySelector():
    return render_template('querySelector.html')

@app.route('/query1')
def queryOne():
    return render_template('query1.html')


def test():
    specialString = ""
    sqlCommand = "select location, year from BQUINTERO.USCrimeAnnualReport where location = 'El Paso, TX'"
    for row in cursor.execute(sqlCommand):
        specialString += str(row) + ", "

    return specialString


@app.route('/results')
def results():
    return render_template('results.html', number=currentQuery, results=test())