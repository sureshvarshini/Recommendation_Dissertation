import os
import csv
from sqlalchemy import Column, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Connect to the food db
engine = create_engine(
    "sqlite:///" + os.path.join(BASE_DIRECTORY, 'food.db'), echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class Food(Base):
    __tablename__ = 'food'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(), nullable=False)
    calories = Column(Float())
    cholesterol = Column(Float())
    folic_acid = Column(Float())
    vitamin_c = Column(Float())
    vitamin_d = Column(Float())
    calcium = Column(Float())
    iron = Column(Float())
    protein = Column(Float())
    carbohydrate = Column(Float())
    fiber = Column(Float())
    sugars = Column(Float())
    fat = Column(Float())


def food_object(row):
    return Food(**row)


def import_food_csv_data(csv_file):
    session = Session()
    print('Checking for any previous records:')
    existing_data = session.query(Food).first()
    if existing_data is None:
        import_data = True
    else:
        import_data = False

    print(f'Previous data found: {import_data}')

    if (import_data):
        with open(csv_file, encoding='utf-8', newline='') as nutrition_file:
            # open and read csv
            csvreader = csv.DictReader(nutrition_file, quotechar='"')

            # Create food object for every row in the csv
            foods = [food_object(row) for row in csvreader]

            # Write to the food database, under food table
            session.add_all(foods)
            session.commit()
