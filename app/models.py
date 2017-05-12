#!/usr/bin/python

from datetime import date
from flask_login import UserMixin
import werkzeug.security as ws

from sqlalchemy import Column, String, Integer, Boolean, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine("sqlite:///KSEF-Nairobi.db")
Base.metadata.bind = engine

class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    role = Column(String)
    fullname = Column(String)
    email = Column(String(120), unique=True)
    username = Column(String(120), unique=True)
    pwhash = Column(String(120))
    is_approved = Column(Boolean, default=False)

class Project(Base):
    __tablename__ = "projects"
    project_id = Column(Integer, primary_key=True)
    subject = Column(String)
    title = Column(String)
    county = Column(String, default="Nairobi")
    zone = Column(String)
    school = Column(String)
    first_presenter = Column(String)
    second_presenter = Column(String, nullable=True)
    score = Column(Float)
    rank = Column(Integer)

Base.metadata.create_all(engine)
