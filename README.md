# abiyabraham1-gmail.com
Cloud Computing
STUDENT NAME: Abraham Abiy
STUDENT NUMBER: ec19462

1) First we start launch aws ec2 instance and access it through Putty

2) Execute the code for the inital GET from the api, using nano to create the file GetFromApi.py

from flask import Flask, render_template, request, jsonify
import json
import requests
import requests_cache
requests_cache.install_cache('crime_api_cache', backend='sqlite', expire_after=36000)
app = Flask(__name__)
street_url_template = 'https://data.police.uk/api/stops-street?lat={lat}&lng={lng}&date={date}' #collecting data from this api

@app.route('/stops-street', methods=['GET'])
def stopchart():
        my_latitude = request.args.get('lat','51.52369')
        my_longitude = request.args.get('lng','-0.0395857')
        my_date = request.args.get('date','2017-12')
        crime_url = street_url_template.format(lat = my_latitude, lng = my_longitude, date = my_date) #specify params of get
        resp = requests.get(crime_url)
        if resp.ok:
                return jsonify(resp.json()) #json response
        else:
                print(resp.reason)
if __name__=="__main__":
        app.run(host='0.0.0.0', debug = True) #specify host and debug

#use 'http://ec2-34-201-72-230.compute-1.amazonaws.com:5000/stops-street' this url to run the get request

3) Next I saved the json into my computer and converted it to a csv so it would be compatible to the table

4) CREATE DATABASE

mkdir CW #create new subdirectory for task
sudo docker pull cassandra:latest #pull Cassandra Docker Image
sudo docker run --name cassandra-CW -p 9042:9042 -d cassandra:latest #Run instance
sudo docker cp stops.csv cassandra-CW:/home/stops.csv #copy csv into container
sudo docker exec -it cassandra-CW cqlsh # access Cassandra command line


CREATE KEYSPACE stops WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};  

CREATE TABLE stops.stats (ID int PRIMARY KEY, age_range text, datetime text, gender text, involved_person boolean, legislation text, location__latitude decimal, location__longitude decimal, location__street__id int, location__street__name text, object_of_search text, officer_defined_ethnicity text, operation boolean, operation_name text, outcome text, outcome_linked_to_object_of_search text, outcome_object__id text, outcome_object__name text, removal_of_more_than_outer_clothing text, self_defined_ethnicity text,type text);

COPY stops.stats(id, age_range, datetime, gender, involved_person, legislation, location__latitude, location__longitude, location__street__id, location__street__name, object_of_search, officer_defined_ethnicity, operation, operation_name, outcome, outcome_linked_to_object_of_search, outcome_object__id, outcome_object__name, removal_of_more_than_outer_clothing, self_defined_ethnicity,type)  FROM 'home/stops.csv' WITH DELIMITER=',' AND HEADER=TRUE;

5)Create file for requirements of the task using, nano requirements.txt 

pip
Flask
cassandra-driver

6)Create Dockerfile using, nano Dockerfile 

FROM python:3.7-alpine
WORKDIR /myapp
COPY . /myapp
RUN pip install -U -r requirements.txt
EXPOSE 8080
CMD ["python" , "app.py"]

7) Use this command to find your ip address which is required for the app file

sudo docker inspect cassandra-CW 

8) (RESTful API)Create file to execute post, get, put and delete requests from the databse using Cassandra queries with flask, using nano app.py

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
                                where id = {}""".format(id)) #select query
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


@app.route('/post/<id>', methods = ['GET', 'POST']) #Post method to db using select and insert query
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



@app.route('/put/<id>', methods = ['GET', 'PUT') #Put method to db using select and update query
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

#add id to url to execute request

8) build and run instance 
sudo docker build . --tag=cassandrarest:v1
sudo docker run -p 80:80 cassandrarest:v1
