from core import app
from flask import Flask, render_template

from flask import Flask, render_template, redirect, url_for, request, session
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, DateField, SelectField, IntegerField, validators
from wtforms.validators import DataRequired, Length

import secrets
foo = secrets.token_urlsafe(16)
app.secret_key = foo

import oracledb
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, Label, Legend, LabelSet, Range1d
from bokeh.embed import components
from bokeh.io import curdoc


currentQuery = 1
thingName = ""

connection = oracledb.connect(user="obisset", password="B69SI5SeQAugPl6lHcd5YrL4", dsn="oracle.cise.ufl.edu:1521/orcl")
cursor = connection.cursor()


# Bootstrap-Flask requires this line
bootstrap = Bootstrap5(app)
# Flask-WTF requires this line
csrf = CSRFProtect(app)

class query1Form(FlaskForm): # Query: Compare the crime rate growth in Chicago vs the US over time (for different crime categories).
    # fromDate = SelectField(u'From', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015])
    fromDate = IntegerField('From Year: ',validators=[
        validators.NumberRange(min=2001, max=2015),  # Adjust min and max as needed
    ])
    # toDate = SelectField(u'To', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015])
    toDate = IntegerField('To Year: ',validators=[
        validators.NumberRange(min=2001, max=2015),  # Adjust min and max as needed
    ])
    crimeType = SelectField(u'Crime Type', choices=["HOMICIDE", "SEX OFFENSE", "ASSAULT", "ROBBERY"])

    submit = SubmitField('Submit')

class query2Form(FlaskForm): #Determine if rain is more likely to decrease crime compared to other weather conditions over a specified period of time.
    # fromDate = DateField('fromDate', format='%Y-%m') #is this doing anything???
    # toDate = DateField('toDate') # FIX LATER

    fromDateYear = SelectField(u'From Year', choices=[2020, 2021, 2022])
    # toDate = SelectField(u'To', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015])
    toDateYear = SelectField(u'To Year', choices=[2020, 2021, 2022])

    fromDateMonth = SelectField(u'From Month', choices=[1,2,3,4,5,6,7,8,9,10,11,12])
    toDateMonth = SelectField(u'To Month', choices=[1,2,3,4,5,6,7,8,9,10,11,12])


    crimeType = SelectField(u'Crime Type', choices=["HOMICIDE", "SEX OFFENSE", "ASSAULT", "ROBBERY"])

    submit = SubmitField('Submit')

class query3Form(FlaskForm): #How has the change in unemployment rates in Chicago over time affected crime rates? 
    # fromDateYear = SelectField(u'From', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016])
    # toDateYear = SelectField(u'To', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016])

    fromDateYear = IntegerField('From Year: ',validators=[
        validators.NumberRange(min=2001, max=2015),  # Adjust min and max as needed
    ])
    # toDate = SelectField(u'To', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015])
    toDateYear = IntegerField('To Year: ',validators=[
        validators.NumberRange(min=2001, max=2015),  # Adjust min and max as needed
    ])

    fromDateMonth = SelectField(u'From Month', choices=[1,2,3,4,5,6,7,8,9,10,11,12])
    toDateMonth = SelectField(u'To Month', choices=[1,2,3,4,5,6,7,8,9,10,11,12])
    # fromDate = SelectField(u'From', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015])
    # toDate = SelectField(u'To', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015])
    # crimeType = SelectField(u'Crime Type', choices=["HOMICIDE", "SEX OFFENSE", "ASSAULT", "ROBBERY"])

    submit = SubmitField('Submit')

class query4Form(FlaskForm):
    # fromDate = SelectField(u'From', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
    # toDate = SelectField(u'To: ', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
    fromDate = IntegerField('From Year: ',validators=[
        validators.NumberRange(min=2001, max=2023),  # Adjust min and max as needed
    ])
    # toDate = SelectField(u'To', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015])
    toDate = IntegerField('To Year: ',validators=[
        validators.NumberRange(min=2001, max=2023),  # Adjust min and max as needed
    ])
    
    crimeRateDate = SelectField(u'Crime Rate Year', choices=[2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023])
    # crimeType = SelectField(u'Crime Type', choices=["HOMICIDE", "SEX OFFENSE", "ASSAULT", "ROBBERY"])

    submit = SubmitField('Submit')

class query5Form(FlaskForm):
    fromDate = IntegerField('From Year: ',validators=[
        validators.NumberRange(min=2001, max=2023),  # Adjust min and max as needed
    ])

    toDate = IntegerField('To Year: ',validators=[
        validators.NumberRange(min=2001, max=2023),  # Adjust min and max as needed
    ])
    

    submit = SubmitField('Submit')

class query6Form(FlaskForm):
    fromDate = IntegerField('From Year: ',validators=[
        validators.NumberRange(min=2001, max=2023),  # Adjust min and max as needed
    ])

    toDate = IntegerField('To Year: ',validators=[
        validators.NumberRange(min=2001, max=2023),  # Adjust min and max as needed
    ])
    
    submit = SubmitField('Submit')


# # Create a Bokeh plot
plot = figure()
plot.add_layout(Legend(), 'right')
# plot = figure(background_color="#ff0000")

curdoc.theme = 'dark_minimal'

year1 = 2002
year2 = 2005

@app.route('/')
def index():
    return render_template('index.html', headline="Hello World!")

# querySelector

@app.route('/querySelector')
def querySelector():
    return render_template('querySelector.html')

@app.route('/query/query1', methods=['GET', 'POST'])
def queryOne():
    global currentQuery
    currentQuery = 1
    form = query1Form()
    message = ""

    if form.validate_on_submit():
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
    global currentQuery
    currentQuery = 2
    form = query2Form()
    if form.validate_on_submit():
        # print("form.toDate.data: " + form.toDate.data)
        # currentQuery = 2
        session['query2FromDateMonth'] = form.fromDateMonth.data
        session['query2FromDateYear'] = form.fromDateYear.data
        session['query2ToDateMonth'] = form.toDateMonth.data
        session['query2ToDateYear'] = form.toDateYear.data
        session['query2CrimeType'] = form.crimeType.data
        # session['query2CrimeType'] = form.crimeType.data
        return redirect( url_for('results') )

    return render_template('query/query2.html', messages = "", form=form)

@app.route('/query/query3', methods=['GET', 'POST'])
def queryThree():
    global currentQuery
    currentQuery = 3
    form = query3Form()

    if form.validate_on_submit(): 
        session['query3FromMonth'] = form.fromDateMonth.data
        session['query3FromYear'] = form.fromDateYear.data
        session['query3ToMonth'] = form.toDateMonth.data
        session['query3ToYear'] = form.toDateYear.data
        return redirect( url_for('results'))

    return render_template('query/query3.html', messages = "", form=form)

@app.route('/query/query4', methods=['GET', 'POST'])
def queryFour():
    global currentQuery
    currentQuery = 4
    form = query4Form()

    if form.validate_on_submit():
        print("form.toDate.data: " + str(form.toDate.data))
        session['query4FromDate'] = form.fromDate.data
        session['query4ToDate'] = form.toDate.data
        session['query4CrimeRateYear'] = form.crimeRateDate.data
        
        # session['query1CrimeType'] = form.crimeType.data
        return redirect( url_for('results') )

    return render_template('query/query4.html', messages = "", form=form)

@app.route('/query/query5', methods=['GET', 'POST'])
def queryFive():
    global currentQuery
    currentQuery = 5
    form = query5Form()

    if form.validate_on_submit(): 
        session['query5FromYear'] = form.fromDate.data
        session['query5ToYear'] = form.toDate.data
        return redirect( url_for('results'))

    return render_template('query/query5.html', messages = "", form=form)

@app.route('/query/query6', methods=['GET', 'POST'])
def querySix():
    global currentQuery
    currentQuery = 6
    form = query6Form()

    if form.validate_on_submit(): 
        session['query6FromYear'] = form.fromDate.data
        session['query6ToYear'] = form.toDate.data
        return redirect( url_for('results'))

    return render_template('query/query6.html', messages = "", form=form)

def plotGraph(): # For putting things into the bokth thingy
    #specialString = ""
    list = []
    plot.renderers = []
    plot.legend.items = []

    # global year1 = 
    # print("currentQuery: " + currentQuery)
    if(currentQuery == 1):
        year1 = session['query1FromDate']
        year2 = session['query1ToDate']
        crimeType = session['query1CrimeType'] 
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
        label = LabelSet(x='x', y='y', text='names', x_offset=5, y_offset=5, x_units='screen', y_units='screen',)
        
        x = []
        y1 = []
        y2 = []
        # plot.clear() #Clear the plot???
        for row in cursor.execute(sqlCommand):
            #specialString += str(row) + ", "
            list.append([row[0],row[1],row[2]])
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
    elif(currentQuery == 2):
        fromMonth = session['query2FromDateMonth']
        fromYear = session['query2FromDateYear']
        toMonth = session['query2ToDateMonth']
        toYear = session['query2ToDateYear']
        crimeType = session['query2CrimeType']

        # print(str(year2Year) + " year2Year")

        sqlCommand = """SELECT hd.year, hd.month, hd.homicide_death_count AS homicide_death_count, cd.covid_death_count AS covid_death_count 
            FROM
            (SELECT year AS year, month AS month, COUNT(caseNumber) AS homicide_death_count
            FROM "C.NGUYEN2".ChicagoCrimeCase
            WHERE crimeType = 'HOMICIDE'
            GROUP BY year, month) hd
            JOIN
            (SELECT year AS year, month AS month, COUNT(caseCount) AS covid_death_count
            FROM BQUINTERO.ChicagoCOVIDReport
            GROUP BY year, month) cd ON hd.year = cd.year AND hd.month = cd.month
            WHERE hd.year < """ + str(toYear) + """ AND hd.year > """ + str(fromYear) + """ OR ((hd.year = """ + str(toYear) +""" AND hd.month < """ + str(toMonth) + """) OR (hd.year = """ + str(fromYear) + """ AND hd.month > """ + str(fromMonth) + """))
            ORDER BY hd.year, hd.month

        """

        # plot.clear() #Clear the plot???

        x = []
        y1 = []
        y2 = []

        for row in cursor.execute(sqlCommand):
            #specialString += str(row) + ", "
            thing = sqlCommand[2]
            # print(row[0])
            
            list.append([row[0],row[1],row[2],row[3]])
            plot.circle([row[0] + row[1] / float(12)], [row[2]], color = "skyblue", legend_label="Homiside Rate")
            plot.circle([row[0] + row[1] / float(12)], [row[3]], color = "red", legend_label="Covid Death Rate")

    elif(currentQuery == 3):
        fromYear = session['query3FromYear']
        fromMonth = session['query3FromMonth']
        fromNumber = (int(fromYear) * 12) + int(fromMonth)
        
        toYear = session['query3ToYear']
        toMonth = session['query3ToMonth']
        toNumber = (int(toYear) * 12) + int(toMonth)

        #x is years, y1 is the crime rate, y2 is the unemployment rate
        x = []
        y1 = []
        y2 = []

        sqlCommand = """SELECT year, month, round(crime_count/pop*100000, 7) AS crime_rate, unemployment_rate
            FROM
            (
                ((SELECT year as y, month, count(*) as crime_count
                FROM "C.NGUYEN2".ChicagoCrimeCase
                GROUP BY Year, Month
                HAVING (year*12 + month) >= """ + str(fromNumber) + """ AND (year*12 + month) <= """ + str(toNumber) + """
                )
                JOIN BQUINTERO.ChicagoPOP
                ON y = BQUINTERO.ChicagoPOP.year)
                
                JOIN
                (SELECT year as y2, month as m2, rate as unemployment_rate
                FROM BQUINTERO.ChicagoUnemploymentReport)
                ON year = y2 AND month = m2
            )
            ORDER BY Year ASC, month ASC
        """

        for row in cursor.execute(sqlCommand):
            list.append([row[0],row[1],row[2],row[3]])
            plot.circle([row[0] + (row[1] / float(12))], [row[2]], color = "red", legend_label="crime rate")
            plot.circle([row[0] + (row[1] / float(12))], [row[3]*200], color = "skyblue", legend_label="scaled unemployment rate")
            x.append([row[0]+row[1]/float(12)])
            y1.append([row[2]])
            y2.append([row[3]*200])
            

        plot.line(x,y1, line_color = "red")
        plot.line(x,y2)
        plot.xaxis[0].axis_label = 'Years, Months'
        plot.yaxis[0].axis_label = 'Rates'

        
    elif(currentQuery == 4):
        fromYear = session['query4FromDate']
        toYear = session['query4ToDate']
        midYear = session['query4CrimeRateYear']
        print("midYear: " + str(midYear))
        x = []
        y = []

        sqlDistrict = """With dist (comm, cnum) AS
            (SELECT "C.NGUYEN2".ChicagoCrimeCase.community AS comm, COUNT("C.NGUYEN2".ChicagoCrimeCase.caseNumber) AS cnum
            FROM "C.NGUYEN2".ChicagoCrimeCase
            WHERE "C.NGUYEN2".ChicagoCrimeCase.year = """ + str(midYear) + """ AND "C.NGUYEN2".ChicagoCrimeCase.community IS NOT NULL
            GROUP BY "C.NGUYEN2".ChicagoCrimeCase.community)
            SELECT comm
            FROM dist
            WHERE cnum = (SELECT MAX(cnum) FROM dist)
            GROUP by comm"""
        for row in cursor.execute(sqlDistrict):
            print("communityNum: " + str(row[0]))

        sqlCommand = """SELECT cp.year AS year, ROUND(cp.cnum*100000/BQUINTERO.CHICAGOPOP.pop,7) AS rate_C
            FROM
            (SELECT "C.NGUYEN2".ChicagoCrimeCase.year AS year, COUNT("C.NGUYEN2".ChicagoCrimeCase.caseNumber) AS cnum
            FROM "C.NGUYEN2".ChicagoCrimeCase 
            JOIN 
            (WITH badComm AS (SELECT "C.NGUYEN2".ChicagoCrimeCase.community AS comm, COUNT("C.NGUYEN2".ChicagoCrimeCase.caseNumber) AS cnum
            FROM "C.NGUYEN2".ChicagoCrimeCase
            WHERE "C.NGUYEN2".ChicagoCrimeCase.year = """ + str(midYear) + """  AND "C.NGUYEN2".ChicagoCrimeCase.community IS NOT NULL 
            GROUP BY "C.NGUYEN2".ChicagoCrimeCase.community)
            SELECT comm AS bc, cnum AS num
            FROM badComm
            WHERE cnum = (SELECT MAX(cnum) FROM badComm)) b
            ON "C.NGUYEN2".ChicagoCrimeCase.community = b.bc 
            WHERE "C.NGUYEN2".ChicagoCrimeCase.year >= """ + str(fromYear) + """ AND "C.NGUYEN2".ChicagoCrimeCase.year <= """ + str(toYear) + """
            GROUP BY "C.NGUYEN2".ChicagoCrimeCase.year) cp JOIN BQUINTERO.CHICAGOPOP ON BQUINTERO.CHICAGOPOP.year = cp.year
            ORDER BY cp.year"""
        for row in cursor.execute(sqlCommand):
            #specialString += str(row) + ", "
            list.append([row[0],row[1]])
            # thing = sqlCommand[2]
            # print(row[0])
            plot.circle([row[0]], [row[1]], color = "skyblue", legend_label="Crime Rate")
            # plot.circle([row[0] + row[1] / float(12)], [row[3]], color = "red", legend_label="Covid Death Rate")
            x.append([row[0]])
            y.append([row[1]])


        plot.line(x,y)
        plot.xaxis[0].axis_label = 'Years'
        plot.yaxis[0].axis_label = 'Crime Rate'


    elif(currentQuery == 5):
        print("FKLQEFLKFJKQDLKFDE")
        fromYear = session['query5FromYear']
        toYear = session['query5ToYear']

        sqlCommand = """SELECT cp.pd AS police_District, cp.year AS year, ROUND(cp.cnum*100000/BQUINTERO.CHICAGOPOP.pop,7) AS rate_C, ave.aveCr AS average_Crime_Rate
            FROM
            (SELECT c.policeDistrict AS pd, c.year AS year, COUNT(c.caseNumber) AS cnum
            FROM "C.NGUYEN2".ChicagoCrimeCase c
            WHERE c.policeDistrict IN
            (
            WITH arrested AS (SELECT c.policeDistrict AS pd, ROUND(COUNT(c.caseNumber)/pddom.dom,5) AS arrestedDom  
            FROM "C.NGUYEN2".ChicagoCrimeCase c JOIN (SELECT c.policeDistrict AS pd, COUNT(c.caseNumber) AS dom
            FROM "C.NGUYEN2".ChicagoCrimeCase c
            WHERE c.isDomestic = 'TRUE'
            GROUP BY c.policeDistrict) pddom on pddom.pd = c.policeDistrict 
            WHERE c.isDomestic = 'TRUE' AND c.isArrested = 'TRUE'
            GROUP BY c.policeDistrict, pddom.dom)
            SELECT c.policeDistrict AS pd
            FROM "C.NGUYEN2".ChicagoCrimeCase c JOIN arrested ON c.policeDistrict = arrested.pd
            WHERE arrested.arrestedDom > (SELECT AVG(arrestedDom) FROM arrested)
            GROUP BY c.policeDistrict)
            GROUP BY c.policeDistrict, c.year
            ORDER BY c.policeDistrict) cp JOIN BQUINTERO.CHICAGOPOP ON BQUINTERO.CHICAGOPOP.year = cp.year
            JOIN (SELECT cp.year AS year, ROUND((cp.cnum*100000/BQUINTERO.CHICAGOPOP.pop)/22,7) AS aveCr
            FROM
            (SELECT c.year AS year, COUNT(c.caseNumber) AS cnum
            FROM "C.NGUYEN2".ChicagoCrimeCase c
            GROUP BY c.year) cp JOIN BQUINTERO.CHICAGOPOP ON BQUINTERO.CHICAGOPOP.year = cp.year) ave ON ave.year = cp.year 
            WHERE cp.year >= """ + str(fromYear) + """ AND cp.year <= """ + str(toYear) 

        districtCounter = 0
        interval = toYear - fromYear

        district8 = []
        district9 = []
        district10 = []
        district12 = []
        district14 = []
        district16 = []
        district17 = []
        district19 = []
        district20 = []
        district24 = []
        district25 = []

        distAdv = []

        year = []

        for i in range(fromYear, toYear + 1):
            year.append(i)

        for row in cursor.execute(sqlCommand):
            #specialString += str(row) + ", "
            list.append([row[0],row[1],row[2],row[3]])
            if row[0] == 8:
                # year.append(row[1])
                district8.append(row[2])
                distAdv.append(row[3])
                plot.circle([row[1]], [row[2]], color = "darkviolet", legend_label="Crime Rate in District " +str(row[0]))
            elif row[0] == 9:
                # year.append(row[1])
                district9.append(row[2])
                plot.circle([row[1]], [row[2]], color = "yellow", legend_label="Crime Rate in District " + str(row[0]))
            elif row[0] == 10:
                # year.append(row[1])
                district10.append(row[2])
                plot.circle([row[1]], [row[2]], color = "green", legend_label="Crime Rate in District " + str(row[0]))
            elif row[0] == 12:
                # year.append(row[1])
                district12.append(row[2])
                plot.circle([row[1]], [row[2]], color = "black", legend_label="Crime Rate in District " + str(row[0]))
            elif row[0] == 14:
                # year.append(row[1])
                district14.append(row[2])
                plot.circle([row[1]], [row[2]], color = "purple", legend_label="Crime Rate in District " +str(row[0]))
            elif row[0] == 16:
                # year.append(row[1])
                district16.append(row[2])
                plot.circle([row[1]], [row[2]], color = "goldenrod", legend_label="Crime Rate in District " +str(row[0]))
            elif row[0] == 17:
                # year.append(row[1])
                district17.append(row[2])
                plot.circle([row[1]], [row[2]], color = "blue", legend_label="Crime Rate in District " +str(row[0]))
            elif row[0] == 19:
                # year.append(row[1])
                district19.append(row[2])
                plot.circle([row[1]], [row[2]], color = "maroon", legend_label="Crime Rate in District " +str(row[0]))
            elif row[0] == 20:
                # year.append(row[1])
                district20.append(row[2])
                plot.circle([row[1]], [row[2]], color = "deeppink", legend_label="Crime Rate in District " +str(row[0]))
            elif row[0] == 24:
                # year.append(row[1])
                district24.append(row[2])
                plot.circle([row[1]], [row[2]], color = "skyblue", legend_label="Crime Rate in District " +str(row[0]))
            elif row[0] == 25:
                # year.append(row[1])
                district25.append(row[2])
                plot.circle([row[1]], [row[2]], color = "mediumspringgreen", legend_label="Crime Rate in District " +str(row[0]))

            # print(row[0])
            #plot.circle([row[1]], [row[2]], color = "skyblue", legend_label="Crime Rate in District " + str(row[0]))
        print("Hi there")
        print(str(len(year)) + " " + str(len(district8)))
        plot.line(year, district8, line_color = "darkviolet")
        plot.line(year, district9, line_color = "yellow")
        plot.line(year, district10, line_color = "green")
        plot.line(year, district12, line_color = "black")
        plot.line(year, district14, line_color = "purple")
        plot.line(year, district16, line_color = "goldenrod")
        plot.line(year, district17, line_color = "blue")
        plot.line(year, district19, line_color = "maroon")
        plot.line(year, district20, line_color = "deeppink")
        plot.line(year, district24, line_color = "skyblue")
        plot.line(year, district25, line_color = "mediumspringgreen")

        plot.line(year, distAdv, line_color = "red", line_width = 3, legend_label="Average Crime Rate") #Working on this
    #return specialString
    return list


    # elif currentQuery == 6: 
    #     print("FKLQEFLKFJKQDLKFDE")
    #     fromYear = session['query6FromYear']
    #     toYear = session['query6ToYear']

    #     sqlCommand = """SELECT cp.pd AS police_District, cp.year AS year, ROUND(cp.cnum*100000/BQUINTERO.CHICAGOPOP.pop,7) AS rate_C, ave.aveCr AS average_Crime_Rate
    #         FROM
    #         (SELECT c.policeDistrict AS pd, c.year AS year, COUNT(c.caseNumber) AS cnum
    #         FROM "C.NGUYEN2".ChicagoCrimeCase c
    #         WHERE c.policeDistrict IN
    #         (
    #         WITH arrested AS (SELECT c.policeDistrict AS pd, ROUND(COUNT(c.caseNumber)/pddom.dom,5) AS arrestedDom  
    #         FROM "C.NGUYEN2".ChicagoCrimeCase c JOIN (SELECT c.policeDistrict AS pd, COUNT(c.caseNumber) AS dom
    #         FROM "C.NGUYEN2".ChicagoCrimeCase c
    #         WHERE c.isDomestic = 'TRUE'
    #         GROUP BY c.policeDistrict) pddom on pddom.pd = c.policeDistrict 
    #         WHERE c.isDomestic = 'TRUE' AND c.isArrested = 'TRUE'
    #         GROUP BY c.policeDistrict, pddom.dom)
    #         SELECT c.policeDistrict AS pd
    #         FROM "C.NGUYEN2".ChicagoCrimeCase c JOIN arrested ON c.policeDistrict = arrested.pd
    #         WHERE arrested.arrestedDom > (SELECT AVG(arrestedDom) FROM arrested)
    #         GROUP BY c.policeDistrict)
    #         GROUP BY c.policeDistrict, c.year
    #         ORDER BY c.policeDistrict) cp JOIN BQUINTERO.CHICAGOPOP ON BQUINTERO.CHICAGOPOP.year = cp.year
    #         JOIN (SELECT cp.year AS year, ROUND((cp.cnum*100000/BQUINTERO.CHICAGOPOP.pop)/22,7) AS aveCr
    #         FROM
    #         (SELECT c.year AS year, COUNT(c.caseNumber) AS cnum
    #         FROM "C.NGUYEN2".ChicagoCrimeCase c
    #         GROUP BY c.year) cp JOIN BQUINTERO.CHICAGOPOP ON BQUINTERO.CHICAGOPOP.year = cp.year) ave ON ave.year = cp.year 
    #         WHERE cp.year >= """ + str(fromYear) + """ AND cp.year <= """ + str(toYear) 

    #     districtCounter = 0
    #     interval = toYear - fromYear

    #     district8 = []
    #     district9 = []
    #     district10 = []
    #     district12 = []
    #     district14 = []
    #     district16 = []
    #     district17 = []
    #     district19 = []
    #     district20 = []
    #     district24 = []
    #     district25 = []

    #     distAdv = []

    #     year = []

    #     for i in range(fromYear, toYear + 1):
    #         year.append(i)

    #     for row in cursor.execute(sqlCommand):
    #         #specialString += str(row) + ", "
    #         list.append([row[0],row[1],row[2],row[3]])
    #         if row[0] == 8:
    #             # year.append(row[1])
    #             district8.append(row[2])
    #             distAdv.append(row[3])
    #             plot.circle([row[1]], [row[2]], color = "darkviolet", legend_label="Crime Rate in District " +str(row[0]))
    #         elif row[0] == 9:
    #             # year.append(row[1])
    #             district9.append(row[2])
    #             plot.circle([row[1]], [row[2]], color = "yellow", legend_label="Crime Rate in District " + str(row[0]))
    #         elif row[0] == 10:
    #             # year.append(row[1])
    #             district10.append(row[2])
    #             plot.circle([row[1]], [row[2]], color = "green", legend_label="Crime Rate in District " + str(row[0]))
    #         elif row[0] == 12:
    #             # year.append(row[1])
    #             district12.append(row[2])
    #             plot.circle([row[1]], [row[2]], color = "black", legend_label="Crime Rate in District " + str(row[0]))
    #         elif row[0] == 14:
    #             # year.append(row[1])
    #             district14.append(row[2])
    #             plot.circle([row[1]], [row[2]], color = "purple", legend_label="Crime Rate in District " +str(row[0]))
    #         elif row[0] == 16:
    #             # year.append(row[1])
    #             district16.append(row[2])
    #             plot.circle([row[1]], [row[2]], color = "goldenrod", legend_label="Crime Rate in District " +str(row[0]))
    #         elif row[0] == 17:
    #             # year.append(row[1])
    #             district17.append(row[2])
    #             plot.circle([row[1]], [row[2]], color = "blue", legend_label="Crime Rate in District " +str(row[0]))
    #         elif row[0] == 19:
    #             # year.append(row[1])
    #             district19.append(row[2])
    #             plot.circle([row[1]], [row[2]], color = "maroon", legend_label="Crime Rate in District " +str(row[0]))
    #         elif row[0] == 20:
    #             # year.append(row[1])
    #             district20.append(row[2])
    #             plot.circle([row[1]], [row[2]], color = "deeppink", legend_label="Crime Rate in District " +str(row[0]))
    #         elif row[0] == 24:
    #             # year.append(row[1])
    #             district24.append(row[2])
    #             plot.circle([row[1]], [row[2]], color = "skyblue", legend_label="Crime Rate in District " +str(row[0]))
    #         elif row[0] == 25:
    #             # year.append(row[1])
    #             district25.append(row[2])
    #             plot.circle([row[1]], [row[2]], color = "mediumspringgreen", legend_label="Crime Rate in District " +str(row[0]))

    #         # print(row[0])
    #         #plot.circle([row[1]], [row[2]], color = "skyblue", legend_label="Crime Rate in District " + str(row[0]))
    #     print("Hi there")
    #     print(str(len(year)) + " " + str(len(district8)))
    #     plot.line(year, district8, line_color = "darkviolet")
    #     plot.line(year, district9, line_color = "yellow")
    #     plot.line(year, district10, line_color = "green")
    #     plot.line(year, district12, line_color = "black")
    #     plot.line(year, district14, line_color = "purple")
    #     plot.line(year, district16, line_color = "goldenrod")
    #     plot.line(year, district17, line_color = "blue")
    #     plot.line(year, district19, line_color = "maroon")
    #     plot.line(year, district20, line_color = "deeppink")
    #     plot.line(year, district24, line_color = "skyblue")
    #     plot.line(year, district25, line_color = "mediumspringgreen")

    #     plot.line(year, distAdv, line_color = "red", line_width = 3, legend_label="Average Crime Rate") #Working on this

    # #return specialString
    # return list

@app.route('/results')
def results():
    #plotGraph() COMMENTED OUT
    result = plotGraph()
    # Generate components for embedding
    script, div = components(plot)
    # year1 = 2003
    # thing = request.args.get('name')

    # plot.show()
    # print(script)
    #return render_template('results.html', number=currentQuery, results=getResults(), thing=thingName, script=script, div=div)
    return render_template('results.html', number=currentQuery, results=result, thing=thingName, script=script, div=div)


app.run()
