"""To avoid confusion between the SQLAlchemy models and the Pydantic models, 
we will have the file models.py with the SQLAlchemy models, 
and the file schemas.py with the Pydantic models"""

"""This file creates the model or schema for the table Records in our database.
"""

import os
from fastapi import APIRouter
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker 
#from sqlalchemy import *
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .upload_file import Base


class Judge(Base):
    __tablename__ = 'judge'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    trump_appointed = Column(Boolean)
    date_appointed = Column(String)
    county = Column(String)
    birth_date = Column(String)
    biography = Column(String)
    # judge can have multiple cases 
    # on using backref it establishes .judge attribute on Case
    cases = relationship("case", backref='judge') # Case.judge 


class Case(Base):
    __tablename__ = 'case'

    id = Column(String, primary_key=True)
    case_id = Column(Integer)
    case_url = Column(String)
    court_type = Column(String)
    hearing_type = Column(String)
    credibility_of_refugee = Column(String)
    refugee_origin = Column(String)
    hearing_location = Column(String)
    protected_ground = Column(String)
    hearing_date = Column(String)
    decision_date = Column(String)
    social_group_type = Column(String)
    # Using foreign key 
    judge_id = Column(Integer, ForeignKey(Judge.id))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    avatarUrl = Column(String)
    password = Column(String)
    role = Column(String)


class BookMarkJudge(Base):
    __tablename__ = 'book_mark_judge'

    id = Column(Integer, primary_key=True)
    # using foreign key 
    user_id = Column(Integer, ForeignKey(User.id))
    # There could be multiple judges bookmarked
    judges = relationship("judge", backref='book_mark_judge') # Judge.book_mark_judge


class BookMarkCase(Base):
    __tablename__ = 'book_mark_case'

    id = Column(Integer, primary_key=True)
    # using foreign key 
    user_id = Column(Integer, ForeignKey(User.id))
    # There could be multiple cases bookmarked
    cases = relationship("case", backref='book_mark_case') # Case.book_mark_case


