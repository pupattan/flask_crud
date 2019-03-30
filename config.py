from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = 'this-is-a-crud-application'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teams.sqlite3'
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
db = SQLAlchemy(app)


