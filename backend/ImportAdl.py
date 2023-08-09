from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Text, Integer, String, JSON,  create_engine
import os
import re
import csv
import pandas as pd
import warnings
from datetime import datetime
warnings.filterwarnings("ignore")

BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


# Connect to the profile db
engine = create_engine(
    "sqlite:///" + os.path.join(BASE_DIRECTORY, 'adl.db'), echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class ADL(Base):
    __tablename__ = 'adl'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer())
    activity = Column(String())
    start_datetime = Column(String())
    end_datetime = Column(String())
    duration = Column(Integer())

def adl_activity_object(row):
    return ADL(**row)


def write_to_db(csv_file):
    print("Importing ADL csv data.")
    session = Session()
    
    with open(csv_file, encoding='utf-8', newline='') as file:
        # open and read csv
        csvreader = csv.DictReader(file, quotechar='"')

        # Create food object for every row in the csv
        adl_activities = [adl_activity_object(row) for row in csvreader]

        # Write to the adl database, under adl table
        session.add_all(adl_activities)
        session.commit()