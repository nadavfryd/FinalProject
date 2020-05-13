
### ----------------------------------------------------------- ###
### --- include all software packages and libraries needed ---- ###
### ----------------------------------------------------------- ###
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms import Form, BooleanField, PasswordField
from wtforms import TextField, TextAreaField, SelectField, DateField
from wtforms import validators, ValidationError

from wtforms.validators import DataRequired

from os import path
import io

import pandas as pd
import numpy as np

import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from wtforms import TextField, TextAreaField, SelectField, DateField, SelectMultipleField, IntegerField


### ----------------------------------------------------------- ###

    

## This class have the fields that are part of the Login form.
##   This form will get from the user a 'username' and a 'password' and sent to the server
##   to check if this user is authorised to continue
## You can see three fields:
##   the 'username' field - will be used to get the username
##   the 'password' field - will be used to get the password
##   the 'submit' button - the button the user will press to have the 
##                         form be "posted" (sent to the server for process)
class LoginFormStructure(FlaskForm):
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Password:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')



## This class have the fields of a registration form
##   This form is where the user can register himself. It will have sll the information
##   we want to save on a user (general information) and the username ans PW the new user want to have
## You can see three fields:
##   the 'FirstName' field - will be used to get the first name of the user
##   the 'LastName' field - will be used to get the last name of the user
##   the 'PhoneNum' field - will be used to get the phone number of the user
##   the 'EmailAddr' field - will be used to get the E-Mail of the user
##   the 'username' field - will be used to get the username
##   the 'password' field - will be used to get the password
##   the 'submit' button - the button the user will press to have the 
##                         form be "posted" (sent to the server for process)
class UserRegistrationFormStructure(FlaskForm):
    FirstName  = StringField('First name:' , validators = [DataRequired()])
    LastName   = StringField('Last name:' , validators = [DataRequired()])
    PhoneNum   = TextField('Phone number', validators = [DataRequired()])
    EmailAddr = TextField("Email",[validators.Required(), validators.Email("Email isn't valid")])
    username   = StringField('User name:  ' , validators = [DataRequired()])
    password   = PasswordField('Password:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')

## This class have the fields that the user can set, to have the query parameters for analysing the data
##   This form is where the user can set different parameters, depand on your project,
##   that will be used to do the data analysis (using Pandas etc.)
## You can see three fields:
##   The fields that will be part of this form are specific to your project
##   Please complete this class according to your needs
##   the 'submit' button - the button the user will press to have the 
##                         form be "posted" (sent to the server for process)
#class DataParametersFormStructure(FlaskForm):
#    
#    submit = SubmitField('Submit')

class ContactFormStructure(FlaskForm):
    FirstName  = StringField('First name:  ' , validators = [DataRequired()])
    LastName   = StringField('Last name:  ' , validators = [DataRequired()])
    PhoneNumber   = TextField('Phone number', validators = [DataRequired()])
    EMail  = TextField("E-mail",[validators.Required(), validators.Email("Email isn't valid")])
    Message  = TextAreaField('Message:  ' , validators = [DataRequired()])
    submit = SubmitField('Submit')
    

    #giving fields for countries, years and sumbit
class CountriesFormStructure(FlaskForm):
    name  = SelectField('First Country:  ' , validators = [DataRequired()])
    name2   = SelectField('Second Country:  ' , validators = [DataRequired()])
    startYear = SelectField('Start Year: ', validators = [DataRequired()])
    endYear = SelectField('End Year: ', validators = [DataRequired()])
    submit = SubmitField('Submit')

    #convertign the graph in to image
    def plot_to_img(fig):
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
        return pngImageB64String

    #transpose my data frame from columns to rows, for more data and easyier work on the data frame
    def transposeDf(self, df,min_year,max_year):
        df=df.set_index("Country Name")
        df1=pd.DataFrame(columns=["country","year","value"])
        mydict={}
        index=0
        for i in range(min_year,max_year):
            col=df[str(i)]
            for j in range(len(col.keys())):
                    mydict[str(index)]=[col.keys()[j],i,col.values[j]]
                    index+=1
        return pd.DataFrame.from_dict(mydict, orient='index',columns=["country","year","value"])

