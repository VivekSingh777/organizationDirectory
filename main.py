#import models
import json
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from flask import jsonify

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
db = SQLAlchemy(app)

class Employee(db.Model):
	__tablename__ = "employee"
	id = db.Column('admin_id',db.Integer , primary_key=True)
	name = db.Column(db.String(100) , nullable =False)
	designation = db.Column(db.String(100), nullable =False)
	department = db.Column(db.String(100), nullable =False)
	manager_name = db.Column(db.String(100))

	def __init__(self , name , designation, department, manager_name):
		self.name = name
		self.designation = designation
		self.department = department
		self.manager_name = manager_name

	def __repr__(self):
		return '{{ id: {}, name: {}, designation: {}, designation: {}, manager_name: {}}}'.format(self.id, self.name, self.designation, self.department, self.manager_name)

	def as_dict(self):

		return {
		'id':self.id,
		'name':self.name,
		'designation':self.designation,
		'department':self.department,
		'manager_name':self.name if self.manager_name =='' or self.manager_name is None else self.manager_name
		}

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/v1/employee/', methods=['POST','GET'])
def create_record():
	if request.method == 'GET':		
		records = Employee.query.all()
		result = []
		for record in records:
			print(record.as_dict())

			result.append(record.as_dict())
		return json.dumps({'records':result})

	record = request.get_json()

	 #checks for valid values
	if check_valid_record(record):
		if record.get('manager_name','') == '':
			record['manager_name'] = record['name']
		new_record = Employee(record.get('name'), record.get('designation'), record.get('department'), record.get('manager_name'))
		db.session.add(new_record)
		db.session.commit()
		return json.dumps({ "success":True})
	return json.dumps({ "success":False})

@app.route('/v1/employee/<id>', methods=['POST'])
def update_record(id):
	record = request.get_json()
	if check_valid_record(record):
		Employee.query.filter_by(id=id).update({'name':record.get('name'), 'designation':record.get('designation'), 'department':record.get('department'), 'manager_name':record.get('manager_name')})
		db.session.commit()
		return json.dumps({'success': True})
	else:
		return json.dumps({'success': False})

@app.route('/v1/employee/<id>', methods=['DELETE'])
def delete_record(id):
	Employee.query.filter_by(id=id).delete()
	db.session.commit()
	return json.dumps({'success': True})

@app.route('/v1/employee/<query>', methods=['GET'])
def search(query):
	connection = db.session.connection()
	search_query = "SELECT * FROM employee WHERE name LIKE '%{}%' OR designation LIKE '%{}%' OR department like '%{}%' OR manager_name like '%{}%'".format(query,query,query, query)
	result = get_dict_from_result(connection.execute(search_query))
	return json.dumps({"success":True, "records": result})

def get_dict_from_result(data):
    op = []
    for entry in data:
        op.append({'id': entry[0], 'name':entry[1], 'designation':entry[2], 'department':entry[3], 'manager_name':entry[1] if entry[4] =='' or entry[4] is None else entry[4]})
    return op

def check_valid_record( record):
	if record.get('name','') != '' and record.get('designation','') != '' and record.get('department','') != '':
		return True
	else:
		return False

if __name__ == "__main__":
    app.run(debug=True)