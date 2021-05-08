import sys,os,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)
from models import RuEng

from flask import Flask,request
import requests
from models import RuEng,User,db,word_user
from pprint import pprint
from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import sessionmaker,scoped_session
from sqlalchemy.ext.declarative import declarative_base
import polyglot
from polyglot.text import Text, Word
import logging
from sqlalchemy.sql import text,delete,and_
import telebot
from sqlalchemy.ext.automap import automap_base

# import logging.config 
# from log_settings import logger_config
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from flask_sqlalchemy import SQLAlchemy
from prettytable import PrettyTable
engine = create_engine('mysql+pymysql://root:1@localhost:27017/rueng')
session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = session.query_property()
Base.prepare(engine,reflect=True)
