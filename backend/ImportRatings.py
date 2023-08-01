import os
import csv
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Connect to rating db
engine = create_engine(
    "sqlite:///" + os.path.join(BASE_DIRECTORY, 'rating.db'), echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class Rating(Base):
    __tablename__ = 'rating'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    user_id = Column(Integer(), nullable=False)
    food_id = Column(Integer(), nullable=False)
    rating = Column(Integer(), nullable=False)


def rating_object(row):
    return Rating(**row)


def import_rating_csv_data(csv_file):
    session = Session()
    print('Checking for any previous records:')
    existing_data = session.query(Rating).first()
    if existing_data is None:
        import_data = True
    else:
        import_data = False

    print(f'Import data?: {import_data}')

    if (import_data):
        with open(csv_file, encoding='utf-8', newline='') as file:
            # open and read csv
            csvreader = csv.DictReader(file, quotechar='"')

            # Create rating object for every row in the csv
            foods = [rating_object(row) for row in csvreader]

            # Write to rating database, under rating table
            session.add_all(foods)
            session.commit()
