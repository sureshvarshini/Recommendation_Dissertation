import os
import re
import pandas as pd
import warnings
from datetime import datetime
warnings.filterwarnings("ignore")
from sqlalchemy import Column, Float, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


# Connect to the profile db
engine = create_engine(
    "sqlite:///" + os.path.join(BASE_DIRECTORY, 'water.db'), echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class Water(Base):
    __tablename__ = 'water'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer(), nullable=False)
    amount = Column(Float())
    last_entry = Column(DateTime())

def reset_water():
    print("Resetting water intake for the day.")
    session = Session()
    water_intakes = session.query(Water).all()
    for user in water_intakes:
        user.amount = 0
        user.last_entry = datetime.now()
        session.commit()