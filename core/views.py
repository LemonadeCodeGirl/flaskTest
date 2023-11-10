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

from bokeh.plotting import figure, show
from bokeh.embed import components


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

@app.route('/query/query1', methods=['GET', 'POST'])
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

    return render_template('query/query1.html', messages = "", form=form)

@app.route('/query/query2', methods=['GET', 'POST'])
def queryTwo():
    form = NameForm()

    return render_template('query/query2.html', messages = "", form=form)

@app.route('/query/query3', methods=['GET', 'POST'])
def queryThree():
    form = NameForm()

    return render_template('query/query3.html', messages = "", form=form)

@app.route('/query/query4', methods=['GET', 'POST'])
def queryFour():
    form = NameForm()

    return render_template('query/query4.html', messages = "", form=form)

@app.route('/query/query5', methods=['GET', 'POST'])
def queryFive():
    form = NameForm()

    return render_template('query/query5.html', messages = "", form=form)

@app.route('/query/query6', methods=['GET', 'POST'])
def querySix():
    form = NameForm()

    return render_template('query/query6.html', messages = "", form=form)

# Create a Bokeh plot
plot = figure()

sqlCommand1 = "select * from BQUINTERO.USCrimeAnnualReport"
sqlCommand2 = "select * from BQUINTERO.USCrimeAnnualReport"
sqlCommand3 = "select * from BQUINTERO.USCrimeAnnualReport"
sqlCommand4 = "select * from BQUINTERO.USCrimeAnnualReport"
sqlCommand5 = "select * from BQUINTERO.USCrimeAnnualReport"
sqlCommand6 = "select * from BQUINTERO.USCrimeAnnualReport"

def plotGraph():
    
    sqlCommand = "select * from BQUINTERO.USCrimeAnnualReport"
    for row in cursor.execute(sqlCommand):
        thing = sqlCommand[2]
        print(row[0])
        plot.circle([row[0], 2, 3], [row[2], 5, 6])
    # count = 0
    # while(count < 10):
    #     plot.circle([count, 2, 3], [count + 1, 5, 6])
    #     count = count + 1

def getResults():
    if(currentQuery == 1):
        specialString = ""
        sqlCommand = "select * from BQUINTERO.USCrimeAnnualReport"
        for row in cursor.execute(sqlCommand):
            specialString += str(row) + ", "
    return specialString

def test():
    specialString = ""
    sqlCommand = "select location, year from BQUINTERO.USCrimeAnnualReport"# where location = '" + thingName + "'"
    for row in cursor.execute(sqlCommand):
        specialString += str(row) + ", "

    return specialString


@app.route('/results')
def results():
    plotGraph()
    # Generate components for embedding
    script, div = components(plot)

    thing = request.args.get('name')

    # plot.show()
    # print(script)
    return render_template('results.html', number=currentQuery, results=getResults(), thing=thingName, script=script, div=div)