from flask import Flask, request, jsonify, make_response, render_template # framework to build webapps
from flask_sqlalchemy import SQLAlchemy # ORM for database layer abstraction
from flask_marshmallow import Marshmallow # allow db schema creation
from sqlalchemy.exc import IntegrityError # handle this db exception

app = Flask(__name__) #set aplication name
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://levely:Elex.184@35.215.208.159/flaskmysql' # pass db parameters new server
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

@app.route('/') # homePage
def welcome():
    return '<h1>Welcome to my API demo</h1>'

@app.route('/people') # query list of students from db table
def list_people():
    all_people = people.query.all()
    result = peoples_schema.dump(all_people)
    return jsonify(result) # return list in json format

@app.route('/people', methods=['POST'])
def new_person():

    rut = request.json['rut'] # receive data from user and store in variables
    name = request.json['name']
    last_name = request.json['last_name']
    age = request.json['age']
    course = request.json['course']

    new_record = people(rut, name, last_name, age, course) # create new student in db table

    try:
        db.session.add(new_record) # store in db
        db.session.commit() # finalize db operation
    except IntegrityError:
        db.session.rollback()
        return '<h1>This rut already exists!<h1>'

    my_resp = make_response('<h1>Person entry added!</h1>')
    my_resp.headers['warning'] = 'Warning'
    my_resp.status_code = 201
    return my_resp

@app.route('/people/<string:rut>') # query list of students from db table
def list_rut(rut):
    people_rut = people.query.filter_by(rut=rut).first_or_404()
    response = people_schema.jsonify(people_rut)
    return response

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
def delete_person(id):
    delete_record = people.query.get(id) # query by id

    db.session.delete(delete_record) # delete record
    db.session.commit() # finalize record

    return people_schema.jsonify(delete_record)

## ERROR HANDLERS ##

@app.errorhandler(404) # forwards Page Not Found to custom page
def page_not_found(e):
    return render_template('404.html')

@app.errorhandler(400) # forwards Page Not Found to custom page
def page_not_found(e):
    return "Data incorrect - please re-check and try again --> 400 status" #return sample plain text

@app.errorhandler(500) # forwards Page Not Found to custom page
def error_500(e):
    return "This is a server error, please check your data and try again --> 500 status" #return sample plain text

## RUN CONFIG ##

if __name__ == '__main__': # execute app as principal class
    app.run(host='0.0.0.0',port=5555, debug=True) # run mode
