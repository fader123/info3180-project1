from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "change this to be a more random key"
app.config['SQLALCHEMY_DATABASE_URI'] =  "postgresql://snfreermudhzsg:02f7fb66d31c6ec6142b60358cf881811daaeea228703b90b67c365254955622@ec2-54-221-236-144.compute-1.amazonaws.com:5432/d372tk1on5thno"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning

db = SQLAlchemy(app)


UPLOAD_FOLDER ='./app/static/uploads'




app.config.from_object(__name__)
from app import views
