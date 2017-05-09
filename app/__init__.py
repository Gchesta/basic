import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
#csrf = CsrfProtect(app)
app.config["SECRET_KEY"] = "D[\xa5E\x89\x01\xf9"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "KSEF-Nairobi.db")
app.config["DEBUG"] = True

from app import views
