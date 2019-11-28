## What is this?
Sample Applicaiton powered by Python3 and Flask.

You can write a short message (including codes) and publish it.
( First, You have to sign up and log in. )

## Run locally

### Installation
    $ pip3 install -r requirements.txt
installs dependency for this app.

### Setup 
You have to set 2 variables:

	$ export DATABASE_URL=mysql://username:password@localhost/db_name
	$ export DATABASE_URL=mysql+pymysql://username:password@localhost/db_name
	$ export flask_config=development

You create database for sqlite and generate dummy data.

    $ python3 manage.py deploy
    
create full text index.

    $ python manage.py shell

    In [1]: search.create_index()


### Run
You start to run app.

    $ python3 manage.py runserver
    
### Test

    $ python3 manage.py test

## Docker
You can run with Docker.

First, You edit two files( See docker-compose.yml ).
* .env
* .env-mysql

### .env
Write MySQL connection info which is used for the application.

example:

	DATABASE_URL=mysql+pymysql://username:password@mysql/db_name

You can change it.

### .env-mysql
Write MySQL account info which is user for MySQL container initialization.

example:

	MYSQL_ROOT_PASSWORD=root_pass
	MYSQL_DATABASE=db_name
	MYSQL_USER=username
	MYSQL_PASSWORD=password

Change them as you want.


### Run Docker containers
Fetch Images when you dont have them.

	$ docker-compose pull

Run.

	$ docker-compose up 

Run as daemon.

	$ docker-compose up -d



