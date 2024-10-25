"""
documentation
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


class Person(Base):
    __tablename__ = "person"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

class promotion(Base):
    __tablename__ = "promotion"
    id = Column(Integer, primary_key=True)
    description = Column(String(250), nullable=False)
    discount = Column(String(250), nullable=False)
    startTime = Column(String(250), nullable=False)
    endTime = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)
    reservation = Column(String(250), nullable=False)
    createdBy = Column(String(250), nullable=False)

class reservation(Base):
    __tablename__ = "reservation"
    id = Column(Integer, primary_key=True)
    reservedBy = Column(String(250), nullable=False)
    workspace = Column(String(250), nullable=False)
    startTime = Column(String(250), nullable=False)
    endTime = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)
    price = Column(String(250), nullable=False)

class workspace(Base):
    __tablename__ = "workspace"
    id = Column(Integer, primary_key=True)
    type = Column(String(250), nullable=False)
    capacity = Column(String(250), nullable=False)
    hourlyRate = Column(String(250), nullable=False)
    availableSchedules = Column(String(250), nullable=False)
    createdBy = Column(String(250), nullable=False)

class schedule(Base):
    __tablename__ = "schedule"
    id = Column(Integer, primary_key=True)
    openingTime = Column(String(250), nullable=False)
    closingTime = Column(String(250), nullable=False)
    status = Column(String(250), nullable=False)