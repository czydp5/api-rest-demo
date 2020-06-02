from flask import Flask # framework to build webapps
from flask-sqlalchemy import SQLAlchemy # ORM for database layer abstraction
from flask_marshmallow import Marshmallow # allow db schema creation

app = flask(__name__) #set aplication name
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://levely:Elex.184@35.215.208.159/flaskmysql' # pass db parameters
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #skip warning messages on runtime

db = SQLALCHEMY(app) # pass config to database variable
ma = Marshmallow(app) # pass config to schema variable

## DATABASE MODELLING ##

class students(db.Model): # create table with columns below
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(10))
    name = db.Column(db.String(70))
    last_name =db.Column(db.String(70))
    age = db.Column(db.Integer)
    course = db.Column(db.String(70))

    def __init__(self, rut, name, last_name, age, course) # assign incoming data to columns
        self.rut = rut
        self.name = name
        self.last_name = last_name
        self.age = age
        self.course = course
