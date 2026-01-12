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

bash
python run.py
