# models.py
from flask import Flask, Blueprint, render_template, abort
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Acc(Base):

    __tablename__ = 'Accs'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(32), unique=True)
    password = Column(String(32))
    email = Column(String(128), unique=True)
    joined = Column(DateTime)
    status = Column(String) # free or head
    teams = relationship("Team", backref= "acc", lazy= "dynamic")
    users = relationship("User", backref= "acc", lazy= "dynamic")

# Это компания
class Team(Base):

    __tablename__ = 'Teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    joined = Column(DateTime)
    info = Column(String(1000))
    acc_id = Column(Integer, ForeignKey('Accs.id'))

    projects = relationship("Project", backref="team", lazy = "dynamic")


class Project(Base):

    __tablename__ = 'Projects'

    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    team_id = Column(Integer, ForeignKey('Teams.id'))

    tasks = relationship("Task", backref="project", lazy = "dynamic")

association_table = Table('association', Base.metadata,
    Column('Tasks_id', Integer, ForeignKey('Tasks.id')),
    Column('Users_id', Integer, ForeignKey('Users.id')))

class Task(Base):

    __tablename__ = 'Tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(32))
    created = Column(DateTime) #дата создания
    expected = Column(DateTime) #дата окончания
    info = Column(String(5000)) #информация про задание
    status = Column(Integer)
    project_id = Column(Integer, ForeignKey("Projects.id"))

    authors = relationship("User",secondary=association_table, backref="tasks", lazy="dynamic")


class User(Base):

    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    acc_id = Column(Integer, ForeignKey('Accs.id'))
    #task_id = Column(Integer, ForeignKey('Tasks.id'))
    #task_id = relationship("Task",secondary=association_table, back_populates="authors", lazy="dynamic")
    #task_id = Column(Integer)
    #status = Column(String)
    rating = Column(Integer)   #!!!!!Скорость выполнения Пока так!!!!!
