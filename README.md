# TableDataTransfer
<!-- Tech stack -->
Frontend: Angular (for UI)
Backend: Flask (Python SQLAlchemy )
Database: MySQL


<!-- BackEnd -->
<!-- BackEnd Setup (Flask API) -->
Prerequisites
Python 3.x
MySQL (or compatible SQL database)
<!-- Create and activate a virtual environment -->
python -m venv venv
venv\Scripts\activate
<!-- Install dependencies inside server folder-->
pip install flask flask-sqlalchemy pymysql
pip install cryptography
pip install flask-cors
pip install SQLAlchemy
<!-- Update database connection details in app.py -->
SOURCE_DB_URI = 'mysql+pymysql://<username>:<password>@localhost/<source_db>'
DESTINATION_DB_URI = 'mysql+pymysql://<username>:<password>@localhost/<destination_db>'
<!-- Run the Flask application -->
flask run --debug
<!-- http://localhost:5000 -->

<!-- FrontEnd -->
<!-- FrontEnd Setup (Angular) -->
Prerequisites
Node.js & npm
Angular CLI
<!-- Install dependencies inside dataTransfer -->
npm install
<!-- Run the Angular application -->
ng serve

<!-- The UI will be available at  http://localhost:4200 -->



