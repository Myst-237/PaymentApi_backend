from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)

#app configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://akjecvzsaeywvv:15109f1557aa7a0f22eb198f9d6cda41a62b48f3514d95dadb2b8136364ed5cf@ec2-44-205-63-142.compute-1.amazonaws.com:5432/d52brv8dghaq0t'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

from app import views
from app import tasks