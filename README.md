A Flask-based backend application to manage company assets and track their
assignment to employees throughout the asset lifecycle.

Tec-stack used:
Flask
Flask-SQLAlchemy
PostgreSQL
Flask-JWT-Extended
APScheduler


packages used
flask – Web framework
flask-sqlalchemy – ORM for database integration
flask-jwt-extended – JWT-based authentication
psycopg2-binary – PostgreSQL database driver


Models used:
User- Stores user details: name, email, password, role

asset- Stores asset details: asset_tag, name, status

Assignment_track- Tracks asset assignment, release, and history


Role-based authentication (Admin, Asset Manager, Employee)
CRUD operations for assets and employees
Asset assignment and release with validation
Prevention of double assignment
Asset retirement handling
Assignment history (audit log)
Background task for asset return reminders

Blueprints- are used to organize routes into separate modules
Config- file stores database connection details and secret keys

All API routes are tested using 
Includes authentication, asset lifecycle operations, and assignment tracking

to run command required is:
python run.py

To test in postman:
for register: /register
"email": email,
"password": password,
"role": role


for login: /login
"email": email,
"password": password

for assets: /asset (for registering or adding asset)
"asset_tag": any asset tag,
"name": asset name

for assign: /assign
asset_id: asset_id(any asset_id which is created during /asset)
"employee_id": any employee id

for assignment: /assignment
it shows all assignments with asset id, assigned employee
here we user get method

for release: /release/asset_id (the asset_id which we want to rlease)
use put method

for retire: /retire/asset_id(for which asset should be retired)
