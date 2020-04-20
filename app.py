from flask import Flask, request
from cassandra.cluster import Cluster
import json

cluster = Cluster(contact_points=["172.17.0.2"],port=9042)
session = cluster.connect()
app = Flask(__name__)

@app.route('/')
def hello():
        gender = request.args.get("gender","male")
        return('<h1>Suspect is, {}!</h1>'.format(gender))

@app.route('/get/<id>') #Get request from db using select query
def get_stop(id):
        id = int(id)
        rows = session.execute( """Select * From stops.stats
                                where id = {}""".format(id))
        for row in rows:
                return jsonify('success: ID {} date of stop on {}'.format(id, row.datetime)),200

        return jsonify('error: No stop on this day!'), 404


@app.route('/delete/<id>') #Delete request from db using delete query
def delete_stop(id):
        id = int(id)
        rows = session.execute("""Delete From stops.stats where id = {}""".format(id))
        for row in rows:
                return jsonify('error: Entry doesn\'t exist!'), 404
        return jsonify('success: ID {} has beeen deleted!'.format(id)), 200


@app.route('/post/<id>', methods = ['GET', 'POST']) #Post method to db using insert query
def post_stop(id):
        id = int(id)
        rows = session.execute( """Select * From stops.stats
                                where id = {}""".format(id))
        for row in rows:
            if len(row)==0:
                rows = session.execute("""INSERT INTO stops.stats (id, age_range, datetime, gender)
                                                VALUES ({}, '100-120', '2020-04', 'Male)""".format(id))
            else:
                return jsonify('error: Entry already exist'), 409
        return jsonify('success: ID {} has been added!'.format(id)), 201



@app.route('/put/<id>', methods = ['GET', 'PUT') #Put method to db using insert query
def update_stop(id):
        id = int(id)
        rows = session.execute( """Select * From stops.stats
                                where id = {}""".format(id))
        for row in rows:
            if len(row)>0:
                rows = session.execute("""UPDATE stops.stats
                                       Set gender = 'Male'
                                       Where id = {}""".format(id))
                return jsonify('success: ID {} has been updated!'.format(id)), 201
            else:
                return jsonify('error: Entry doesn\'t exists!'), 404



if __name__ == '__main__':
        app.run(host='0.0.0.0',debug=True, port=80)
