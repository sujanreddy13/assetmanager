packages installed are flask

 flask-sqlalchemy used to connect database with flask
 
 flask-jwt-extended for jwt token
 
 psycopg2-binary it is a PostgreSQL database driver for Python.


models is used to create models like to tables to store entered data:
User is model like table table which stores details of user(name, email, password, role).
employee model has fileds like name, email, department 
asset model is used to store assets this include fields like asset_tag, name, status

used Blueprint:
which is used to write code at different files and makes connection between or routes to each. By this the code is written to respective files.

config:
it represents database connection details like secretkeys.

used postman to register and login by CRUD operations

command to run:
python run.py
