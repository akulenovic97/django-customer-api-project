# django-customer-api-project
A basic REST API project built with Django + postgres that parses sample Customer JSON info and inserts/updates it in the database.

## PRE-REQUISITE: Install and set up postgresSQL on your local machine. Set up the database with this information:  
      'NAME': 'customer_db'  
      'USER': 'admin'  
      'PASSWORD': 'test1234'  

## Instructions to install and get Django application running:
1. Create a new Python virtual environment and pip install requirements.txt. Activate the new virtual environment.
2. Adjust the DATABASES definition in customer_api\customer_api\settings.py accordingly if you've set up your database differently.
3. In your terminal, change into the customer_api (with the manage.py file) and run these two commands:
  python manage.py makemigrations vendor_data
  python manage.py migrate
4. Stay in the directory and run the web server with this command:
  python manage.py runserver

Once these steps are run, the API endpoint is running locally and can accept JSON data for POST/PUT operations in your local database.

The POST API endpoint is: http://127.0.0.1:8000/api/customers

The PUT API endpoint is: http://127.0.0.1:8000/api/customers/update

You can use cURL requests if you want to send a JSON file to one of the endpoints:
```
curl -X POST -H "Content-Type: application/json" -d @test_file.json http://127.0.0.1:8000/api/customers
```
```
curl -X POST -H "Content-Type: application/json" -d @test_file.json http://127.0.0.1:8000/api/customers/update
```

You can also use the [Postman](https://www.postman.com/) client to send JSON as well.

## Main components that couldn't be implemented in time
1. Dockerization of the application (kept receiving issue of password authentication, created 'dockerization-try' for later review on implementation).
2. Foreign key implementation on Subscription and Gifts tables.
  Subscription would have customer_id.   
  Gifts should have a new entry in Subscription then have subscription_id and customer_id as foreign keys.
