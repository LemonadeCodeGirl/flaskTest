from core import app
from flask import Flask, render_template

from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

import secrets
foo = secrets.token_urlsafe(16)
app.secret_key = foo

import oracledb

currentQuery = 1
thingName = ""

connection = oracledb.connect(user="obisset", password="B69SI5SeQAugPl6lHcd5YrL4", dsn="oracle.cise.ufl.edu:1521/orcl")
cursor = connection.cursor()


# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

class NameForm(FlaskForm):
    name = StringField('Which actor is your favorite?')
    submit = SubmitField('Submit')

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

@app.route('/query1', methods=['GET', 'POST'])
def queryOne():
    form = NameForm()
    message = ""

    if form.validate_on_submit():
        name = form.name.data
        print(name)
    #     if name.lower() in names:
    #         # empty the form field
    #         form.name.data = ""
    #         id = get_id(ACTORS, name)
    #         # redirect the browser to another route and template

        global thingName
        thingName = name
        print(thingName)
        return redirect( url_for('results', thing=thingName) )
    #     else:
    #         message = "That actor is not in our database."
    # # return render_template('index.html', names=names, form=form, message=message)

    return render_template('query1.html', messages = "", form=form)


def test():
    specialString = ""
    sqlCommand = "select location, year from BQUINTERO.USCrimeAnnualReport where location = 'El Paso, TX'"
    for row in cursor.execute(sqlCommand):
        specialString += str(row) + ", "

    return specialString


@app.route('/results')
def results():
    thing = request.args.get('name')
    print(thingName)
    return render_template('results.html', number=currentQuery, results=test(), thing=thingName)