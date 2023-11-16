from core import app
from flask import Flask, render_template

from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired, Length

import secrets
foo = secrets.token_urlsafe(16)
app.secret_key = foo

import oracledb

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Label, LabelSet, Range1d
from bokeh.embed import components


currentQuery = 1
thingName = ""

connection = oracledb.connect(user="obisset", password="B69SI5SeQAugPl6lHcd5YrL4", dsn="oracle.cise.ufl.edu:1521/orcl")
cursor = connection.cursor()


# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

class query1Form(FlaskForm):
    fromDate = SelectField(u'From', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015])
    toDate = SelectField(u'To', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015])
    crimeType = SelectField(u'Crime Type', choices=["HOMICIDE", "SEX OFFENSE", "ASSAULT", "ROBBERY"])

    submit = SubmitField('Submit')

# qform = query1Form()

# Create a Bokeh plot
plot = figure()

year1 = 2002
year2 = 2005

sqlCommand1 = """SELECT c.year, c.rate_C, us.rate_US 
FROM
(SELECT cp.year AS year, ROUND(cp.cnum*100000/BQUINTERO.CHICAGOPOP.pop,7) AS rate_C
FROM
(SELECT "C.NGUYEN2".ChicagoCrimeCase.year AS year, COUNT("C.NGUYEN2".ChicagoCrimeCase.caseNumber) AS cnum
FROM "C.NGUYEN2".ChicagoCrimeCase
WHERE "C.NGUYEN2".ChicagoCrimeCase.crimeType = 'ROBBERY' AND "C.NGUYEN2".ChicagoCrimeCase.year >= """ + str(year1) + """ AND "C.NGUYEN2".ChicagoCrimeCase.year <= """ + str(year2) + """
GROUP BY "C.NGUYEN2".ChicagoCrimeCase.year) cp JOIN BQUINTERO.CHICAGOPOP ON BQUINTERO.CHICAGOPOP.year = cp.year) c
JOIN
(SELECT BQUINTERO.USCrimeNew.year AS year, BQUINTERO.USCrimeNew.rate AS rate_US
FROM BQUINTERO.USCrimeNew
WHERE BQUINTERO.USCrimeNew.type = 'ROBBERY' AND BQUINTERO.USCrimeNew.year >= """ + str(year1) + """ AND BQUINTERO.USCrimeNew.year <= """ + str(year2) + """) us ON c.year = us.year
ORDER BY c.year"""
sqlCommand2 = "select * from BQUINTERO.USCrimeAnnualReport"
sqlCommand3 = "select * from BQUINTERO.USCrimeAnnualReport"
sqlCommand4 = "select * from BQUINTERO.USCrimeAnnualReport"
sqlCommand5 = "select * from BQUINTERO.USCrimeAnnualReport"
sqlCommand6 = "select * from BQUINTERO.USCrimeAnnualReport"

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
    form = query1Form()
    message = ""

    if form.validate_on_submit():
        print("form.toDate.data: " + form.toDate.data)
        session['query1FromDate'] = form.fromDate.data
        session['query1ToDate'] = form.toDate.data
        session['query1CrimeType'] = form.crimeType.data
        return redirect( url_for('results') )
    #     else:
    #         message = "That actor is not in our database."
    # # return render_template('index.html', names=names, form=form, message=message)

    return render_template('query/query1.html', messages = "", form=form)

@app.route('/query/query2', methods=['GET', 'POST'])
def queryTwo():
    form = query1Form()

    return render_template('query/query2.html', messages = "", form=form)

@app.route('/query/query3', methods=['GET', 'POST'])
def queryThree():
    form = query1Form()

    return render_template('query/query3.html', messages = "", form=form)

@app.route('/query/query4', methods=['GET', 'POST'])
def queryFour():
    form = query1Form()

    return render_template('query/query4.html', messages = "", form=form)

@app.route('/query/query5', methods=['GET', 'POST'])
def queryFive():
    form = query1Form()

    return render_template('query/query5.html', messages = "", form=form)

@app.route('/query/query6', methods=['GET', 'POST'])
def querySix():
    form = query1Form()

    return render_template('query/query6.html', messages = "", form=form)

def plotGraph():
    specialString = ""
    # global year1 = 
    year1 = session['query1FromDate']
    year2 = session['query1ToDate']
    crimeType = session['query1CrimeType'] 

    print(year1)
    sqlCommand = """SELECT c.year, c.rate_C, us.rate_US 
            FROM
            (SELECT cp.year AS year, ROUND(cp.cnum*100000/BQUINTERO.CHICAGOPOP.pop,7) AS rate_C
            FROM
            (SELECT "C.NGUYEN2".ChicagoCrimeCase.year AS year, COUNT("C.NGUYEN2".ChicagoCrimeCase.caseNumber) AS cnum
            FROM "C.NGUYEN2".ChicagoCrimeCase
            WHERE "C.NGUYEN2".ChicagoCrimeCase.crimeType = '""" + str(crimeType) + """' AND "C.NGUYEN2".ChicagoCrimeCase.year >= """ + str(year1) + """ AND "C.NGUYEN2".ChicagoCrimeCase.year <= """ + str(year2) + """
            GROUP BY "C.NGUYEN2".ChicagoCrimeCase.year) cp JOIN BQUINTERO.CHICAGOPOP ON BQUINTERO.CHICAGOPOP.year = cp.year) c
            JOIN
            (SELECT BQUINTERO.USCrimeNew.year AS year, BQUINTERO.USCrimeNew.rate AS rate_US
            FROM BQUINTERO.USCrimeNew
            WHERE BQUINTERO.USCrimeNew.type = '""" + str(crimeType) + """' AND BQUINTERO.USCrimeNew.year >= """ + str(year1) + """ AND BQUINTERO.USCrimeNew.year <= """ + str(year2) + """) us ON c.year = us.year
            ORDER BY c.year"""
    
    # sqlCommand = "select * from BQUINTERO.USCrimeAnnualReport"
    
    label = LabelSet(x='x', y='y', text='names', x_offset=5, y_offset=5, x_units='screen', y_units='screen',)
    
    x = []
    y1 = []
    y2 = []
    for row in cursor.execute(sqlCommand):
        thing = sqlCommand[2]
        # print(row[0])
        plot.circle([row[0]], [row[1]], color = "skyblue", legend_label="Chicago Crime Rate")
        plot.circle([row[0]], [row[2]], color = "red", legend_label="US Crime Rate")

        x.append([row[0]])
        y1.append([row[1]])
        y2.append([row[2]])

    plot.line(x,y1)
    plot.line(x,y2)
    plot.xaxis[0].axis_label = 'Years'
    plot.yaxis[0].axis_label = 'Crime Rates'


def getResults():

    if(currentQuery == 1):
        specialString = ""
        # global year1 = 
        year1 = session['query1FromDate']
        year2 = session['query1ToDate']
        crimeType = session['query1CrimeType'] 

        print(year1)
        sqlCommand = """SELECT c.year, c.rate_C, us.rate_US 
                FROM
                (SELECT cp.year AS year, ROUND(cp.cnum*100000/BQUINTERO.CHICAGOPOP.pop,7) AS rate_C
                FROM
                (SELECT "C.NGUYEN2".ChicagoCrimeCase.year AS year, COUNT("C.NGUYEN2".ChicagoCrimeCase.caseNumber) AS cnum
                FROM "C.NGUYEN2".ChicagoCrimeCase
                WHERE "C.NGUYEN2".ChicagoCrimeCase.crimeType = '""" + str(crimeType) + """' AND "C.NGUYEN2".ChicagoCrimeCase.year >= """ + str(year1) + """ AND "C.NGUYEN2".ChicagoCrimeCase.year <= """ + str(year2) + """
                GROUP BY "C.NGUYEN2".ChicagoCrimeCase.year) cp JOIN BQUINTERO.CHICAGOPOP ON BQUINTERO.CHICAGOPOP.year = cp.year) c
                JOIN
                (SELECT BQUINTERO.USCrimeNew.year AS year, BQUINTERO.USCrimeNew.rate AS rate_US
                FROM BQUINTERO.USCrimeNew
                WHERE BQUINTERO.USCrimeNew.type = '""" + str(crimeType) + """' AND BQUINTERO.USCrimeNew.year >= """ + str(year1) + """ AND BQUINTERO.USCrimeNew.year <= """ + str(year2) + """) us ON c.year = us.year
                ORDER BY c.year"""
        for row in cursor.execute(sqlCommand):
            specialString += str(row) + ", "
    return specialString

@app.route('/results')
def results():
    plotGraph()
    # Generate components for embedding
    script, div = components(plot)
    # year1 = 2003
    # thing = request.args.get('name')

    # plot.show()
    # print(script)
    return render_template('results.html', number=currentQuery, results=getResults(), thing=thingName, script=script, div=div)


app.run()