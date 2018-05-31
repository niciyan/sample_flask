## What is this?
Sample Applicaiton powered by Python3 and Flask.

You can write a short message (including codes) and publish it.
( First, You have to sign up. )


## Demo
You can view this app running on heroku

https://evening-bastion-33772.herokuapp.com/

## Installation
    $ pip3 install -r requirements.txt
installs dependency for this app.

## Setup 
You have to set 2 variables:

	$ export DATABASE_URL=mysql://username:password@localhost/db_name
	$ export DATABASE_URL=mysql+pymysql://username:password@localhost/db_name
	$ export flask_config=development

You create database for sqlite and generate dummy data.

    $ python3 manage.py deploy

## Run
You start to run app.

    $ python3 manage.py runserver
