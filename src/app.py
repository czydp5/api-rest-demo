from flask import Flask, request, jsonify # framework to build webapps
from flask_sqlalchemy import SQLAlchemy # ORM for database layer abstraction
from flask_marshmallow import Marshmallow # allow db schema creation

app = Flask(__name__) #set aplication name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://levely:Elex.184@35.215.208.159/flaskmysql' # pass db parameters
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #skip warning messages on runtime

db = SQLAlchemy(app) # initialize variable
ma = Marshmallow(app) # initialize variable

## DATABASE MODELLING ##

class people(db.Model): # define table with columns below
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

class PeopleSchema(ma.Schema): # set db schema
    class Meta:
        fields = ('id', 'rut', 'name', 'last_name', 'age', 'course')

people_schema = PeopleSchema() # create schema for one value
peoples_schema = PeopleSchema(many=True) # create schema for multiple values

## ENDPOINTS ##

@app.route('/people', methods=['POST'])
def create_people():

    rut = request.json['rut'] # receive data from user and store in variables
    name = request.json['name']
    last_name = request.json['last_name']
    age = request.json['age']
    course = request.json['course']

    new_people = people(rut, name, last_name, age, course) # create new student in db table

    db.session.add(new_people) # store in db
    db.session.commit() # finalize db operation

    return people_schema.jsonify(new_people) # forward data entry view to user

@app.route('/people') # query list of students from db table
def get_peoples():
    all_peoples = people.query.all()
    result = peoples_schema.dump(all_peoples)
    return jsonify(result) # return list in json format

@app.route('/people/<id>', methods=['PUT']) # update student
def update_people(id):
    People = people.query.get(id) # table to be updated

    rut = request.json['rut'] # passing data to current fields
    name = request.json['name']
    last_name = request.json['last_name']
    age = request.json['age']
    course = request.json['course']

    People.rut = rut # update fields
    People.name = name
    People.last_name = last_name
    People.age = age
    People.course = course

    db.session.commit() # save changes
    return people_schema.jsonify(People)

@app.route('/people/<id>', methods=['DELETE'])
def delete_people(id):
    People = people.query.get(id) # query by id

    db.session.delete(People) # delete record
    db.session.commit() # finalize record

    return people_schema.jsonify(People)

## RUN CONFIG ##

if __name__ == "__main__": # execute app as principal class
    app.run(debug = True) # run mode
