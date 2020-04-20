# abiyabraham1-gmail.com
Cloud Computing

STUDENT NAME: Abraham Abiy

STUDENT NUMBER: ec19462

1)First we start launch aws ec2 instance and access it through Putty

2)Execute the code for the inital GET from the api, using nano to create the file GetFromApi.py and using 'http://ec2-34-201-72-230.compute-1.amazonaws.com:5000/stops-street' url to run the get request

3)Next I saved the json into my computer and converted it to a csv so it would be compatible to the table

4)CREATE DATABASE using following commands

mkdir CW #create new subdirectory for task

sudo docker pull cassandra:latest #pull Cassandra Docker Image

sudo docker run --name cassandra-CW -p 9042:9042 -d cassandra:latest #Run instance

sudo docker cp stops.csv cassandra-CW:/home/stops.csv #copy csv into container

sudo docker exec -it cassandra-CW cqlsh # access Cassandra command line


CREATE KEYSPACE stops WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};  

CREATE TABLE stops.stats (ID int PRIMARY KEY, age_range text, datetime text, gender text, involved_person boolean, legislation text, location__latitude decimal, location__longitude decimal, location__street__id int, location__street__name text, object_of_search text, officer_defined_ethnicity text, operation boolean, operation_name text, outcome text, outcome_linked_to_object_of_search text, outcome_object__id text, outcome_object__name text, removal_of_more_than_outer_clothing text, self_defined_ethnicity text,type text);

COPY stops.stats(id, age_range, datetime, gender, involved_person, legislation, location__latitude, location__longitude, location__street__id, location__street__name, object_of_search, officer_defined_ethnicity, operation, operation_name, outcome, outcome_linked_to_object_of_search, outcome_object__id, outcome_object__name, removal_of_more_than_outer_clothing, self_defined_ethnicity,type)  FROM 'home/stops.csv' WITH DELIMITER=',' AND HEADER=TRUE;

5)Create file for requirements of the task using, nano requirements.txt 

6)Create Dockerfile using, nano Dockerfile 

7)sudo docker inspect cassandra-CW' Use this command to find your ip address which is required for the app file 

8)(RESTful API)Create file to execute post, get, put and delete requests from the databse using Cassandra queries with flask, using nano app.py

9) build and run instance 
sudo docker build . --tag=cassandrarest:v1
sudo docker run -p 80:80 cassandrarest:v1

GET: curl -X GET URL/port/get/<id>
  
POST: curl -X POST URL/port/post/<id>
  
PUT: curl -X PUT URL/port/put/<id>
  
DELETE: curl -X URL/port/delete<id>

ALL FILES USED ARE IN REPOSITORY
