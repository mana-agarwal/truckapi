from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
from flask.views import View
import json
from flask_paginate import Pagination, get_page_parameter



mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'truckapi'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

api = Api(app)

@app.route("/display")

def display():
	cur = mysql.connect().cursor()
	cur.execute('''select * from trucks''')
	data=cur.fetchall()
	rows=[]
	for item in data:
		i={'truck_number':str(item[0]), 'latitude':str(item[1]),'longitude':str(item[2]) }
		rows.append(i)
	page = request.args.get(get_page_parameter(), type=int, default=10)
	pagination = Pagination(page=page, total=len(rows), record_name='rows')
	return render_template('trucks.html', objects=rows,pagination=pagination)


@app.route('/get_fields')
def get_fields():
	parser = reqparse.RequestParser()
        parser.add_argument('truck_number', type=str)
        args = parser.parse_args()
        truckno = args['truck_number']
	
	cur = mysql.connect().cursor()
	cur.execute('''select * from trucks where truck_number=%s ''',(truckno))
	data=cur.fetchall()
	print data
	rows=[]
	for item in data:
		i={'truck_number':str(item[0]), 'latitude':str(item[1]),'longitude':str(item[2]) }
		rows.append(i)
        return jsonify(rows)
 

@app.route('/add_truck',methods=["POST"])
def add_truck():
	parser = reqparse.RequestParser()
        parser.add_argument('truck_number', type=str)
	parser.add_argument('latitude', type=str)
	parser.add_argument('longitude', type=str)
        args = parser.parse_args()
        truckno = args['truck_number']
	lat = args['latitude']
	log = args['longitude']	
	if truckno is None:
		return json.dumps({'Message': 'truck number missing'})
	if log is None:
		return json.dumps({'Message': 'longitude missing'})
	if lat is None:
		return json.dumps({'Message': 'latitude missing'})	
	conn=mysql.connect()
	cur = conn.cursor()
	cur.execute('''insert into trucks(truck_number,latitude,longitude) values (%s,%s,%s) ''',(int(truckno), float(lat), float(log)))
	data=cur.fetchall()
	conn.commit()
	return json.dumps({'Message': 'Successful'})

if __name__ == '__main__':
    app.run(debug=True)
