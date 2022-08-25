from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)

#app configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://u7t4i2vsevq6d1:p71c79682e754bada9ea368ed709b95a89fd74795d3aa87191a74125b2631df3b@ec2-3-90-192-74.compute-1.amazonaws.com:5432/dcrauv82ap8t40'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)

from app import views
from app import tasks