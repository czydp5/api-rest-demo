from flask import Flask, request, jsonify # framework to build webapps
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

class StudentSchema(ma.Schema): # set db schema
    class Meta:
        fields = ('id', 'rut', 'name', 'last_name', 'age', 'course')

student_schema = StudentSchema() # create schema for one value
students_schema = StudentSchema(many=True) # create schema for multiple values

## ENDPOINTS ##

@app.route('/students', methods=['POST'])
def create_student():

    rut = request.json['rut'] # receive data from user and store in variables
    name = request.json['name']
    last_name = request.json['last_name']
    age = request.json['age']
    course = request.json['course']

    new_student = student(rut, name, last_name, age, course) # create new student in db table

    db.session.add(new_student) # store in db
    db.session.commit() # finalize db operation

    return student_schema.jsonify(new_student) # forward data entry view to user

@app.route('/students') # query list of students from db table
def get_students():
    all_students = student.query.all()
    result = students_schema.dump(all_students)
    return jsonify(result) # return list in json format

## RUN CONFIG ##

if __name__ == "__main__": # execute app as principal class
    app.run(debug = True) # run mode
