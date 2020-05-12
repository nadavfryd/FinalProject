"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from DemoFormProject import app
from DemoFormProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

import sys

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError


from DemoFormProject.Models.QueryFormStructure import LoginFormStructure 
from DemoFormProject.Models.QueryFormStructure import UserRegistrationFormStructure 
from DemoFormProject.Models.QueryFormStructure import ContactFormStructure 
from DemoFormProject.Models.QueryFormStructure import CountriesFormStructure 

###from DemoFormProject.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser 

db_Functions = create_LocalDatabaseServiceRoutines() 


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Information about the album'
    )

# -------------------------------------------------------
# Register new user page
# -------------------------------------------------------
@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

# -------------------------------------------------------
# Login page
# This page is the filter before the data analysis
# -------------------------------------------------------
@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            return redirect('DataQuery')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/Data')
def Data():
    """Renders the data page."""
    return render_template(
        'Data.html',
        title='Data',
        year=datetime.now().year,
        message='Welcome to my data'
    )


@app.route  ('/DataSet')
def DataSet():
    """Renders the DataSet page."""

    df = pd.read_csv(path.join(path.dirname(__file__), "static\\Data\\API_SL.UEM.TOTL.ZS_DS2_en_csv_v2_887304.csv"), skiprows=4, usecols = ['Country Name','Country Code', 'Indicator Name', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'])

    raw_data_table = ""
    data1 = df.head(31)
    if (request.method == 'POST' and form.validate()):
        raw_data_table = df.to_html(classes = 'table table-hover')

    return render_template(
        'DataSet.html',
        title='DataSet',
        raw_data_table = raw_data_table,
        year=datetime.now().year,
        message='My Data Set', data = data1.to_html(classes = "table table-hover")
    )

@app.route('/album')
def album():
    """Renders the album page."""
    return render_template(
        'album.html',
        title='Album',
        year=datetime.now().year,
    )

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        flash('Thanks for contacting us')

    if (request.method == 'POST' and form.validate()):
            db_Functions.AddContact(form)
            db_table = ""

    return render_template(
        'contact.html', 
        form=form, 
        title='Contact',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/DataQuery', methods = ['GET' , 'POST']
)
def DataQuery():
    """Renders the DataQuery page."""
    form = CountriesFormStructure(request.form)

    df = pd.read_csv(path.join(path.dirname(__file__), "static\\Data\\API_SL.UEM.TOTL.ZS_DS2_en_csv_v2_887304.csv"), skiprows=4, usecols = ['Country Name','Country Code', 'Indicator Name', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019'])

    df2 = df.groupby('Country Name').sum()

    l = df2.index
    m = list(zip(l, l))

    form.name.choices = m
    form.name2.choices = m

    chart = " "
    table1 = " "
    table2 = " "

    if (request.method == 'POST' and form.validate()): 
        name = form.name.data
        name2 = form.name2.data
       
        graph, ax = plt.subplots()

        plt.tight_layout()

        df1 = form.transposeDf(df, 1991, 2020)

        df1 = df1.loc[(df1['country'] == name) | (df1['country'] == name2)]

        countryDataBase1 = df.loc[(df['Country Name'] == name)]
        countryDataBase2 = df.loc[(df['Country Name'] == name2)]

        table1 = countryDataBase1.to_html(classes = "table table-hover")
        table2 = countryDataBase2.to_html(classes = "table table-hover")

        ax.set_ylabel('percentage')
        ax.set_title('Unemployment rate - graph')

        for name, country in df1.groupby("country"):
            country.plot(kind = "line", x = "year", y = "value", ax = ax, label = name, figsize = (7, 6))

        chart = CountriesFormStructure.plot_to_img(graph)

    return render_template(
        'DataQuery.html',
        title='DataQuery',
        form = form,
        chart = chart,
        table1 = table1,
        table2 = table2,
        year=datetime.now().year,
        message='presenting the data'
    )

