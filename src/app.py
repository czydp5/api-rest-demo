from flask import Flask # framework to build webapps
from flask-sqlalchemy import SQLAlchemy # ORM for database layer abstraction
from flask_marshmallow import Marshmallow # allow db schema creation

app = flask(__name__) #set aplication name
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://levely:Elex.184@35.215.208.159/flaskmysql' # pass db parameters
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #skip warning messages on runtime

db = SQLALCHEMY(app) # pass config to database variable
ma = Marshmallow(app) # pass config to schema variable
