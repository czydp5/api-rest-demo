from flask import Flask, request # framework to build webapps
from flask_sqlalchemy import SQLAlchemy # ORM for database layer abstraction
from flask_marshmallow import Marshmallow # allow db schema creation

app = Flask(__name__) #set aplication name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://levely:Elex.184@35.215.208.159/flaskmysql' # pass db parameters
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #skip warning messages on runtime

db = SQLAlchemy(app) # initialize variable
ma = Marshmallow(app) # initialize variable

## DATABASE MODELLING ##

class student(db.Model): # define table with columns below
    id = db.Column(db.Integer, primary_key=True)
    rut = db.Column(db.String(10))
    name = db.Column(db.String(70))
    last_name =db.Column(db.String(70))
    age = db.Column(db.Integer)
    course = db.Column(db.String(70))

    def __init__(self, rut, name, last_name, age, course): # assign incoming data to columns
        self.rut = rut
        self.name = name
        self.last_name = last_name
        self.age = age
        self.course = course

db.create_all() # method to read all classes and create tables

class studentSchema(ma.Schema): # set db schema
    class Meta:
        fields = ('id', 'rut', 'name', 'last_name', 'age', 'course')

student_schema = studentSchema # create variable instance to be used elsewhere

## ENDPOINTS ##

@app.route('/student', methods=['POST'])
def createStudent():

    print(request.json)
    return 'received'

## RUN CONFIG ##

if __name__ == "__main__": # execute app as principal class
    app.run(debug = True) # run mode
