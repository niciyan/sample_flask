## What is this?
Sample Applicaiton powered by Python3 and Flask.


## Demo
You can view this app running on heroku

https://evening-bastion-33772.herokuapp.com/

## Installation
    $ pip install -r requirements.txt
installs dependency for this app.

## Setup 
You have to set 2 variables:

	$ export DATABASE_URL=mysql://username:password@localhost/db_name
	$ export flask_config=development

You create database for sqlite and generate dummy data.

    python manage.py deploy

## Run
You start to runa app.

    $ python manage.py runserver
