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

ADL_RAW_DATASET_LOCATION = os.getcwd(
) + "\\preprocessing\\datasets\\Activity_predictor\\raw\\"

ADL_CSV_DATASET_LOCATION = os.getcwd() + "\\preprocessing\\cleanedDatasets\\ADL\\"


# Connect to the profile db
engine = create_engine(
    "sqlite:///" + os.path.join(BASE_DIRECTORY, 'profile.db'), echo=True)
Base = declarative_base()
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'profile'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    username = Column(String(), nullable=False, unique=True)
    email = Column(String(), nullable=False)
    password = Column(Text(), nullable=False)
    firstname = Column(String())
    lastname = Column(String())
    age = Column(Integer())
    gender = Column(String())
    height = Column(Integer())
    weight = Column(Integer())
    illness = Column(String())
    activity_level = Column(String())
    schedule = Column(JSON())
    mobilityscore = Column(Integer()) 


class Activity(Base):
    __tablename__ = 'activity'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(), nullable=False)
    type = Column(String())
    directions = Column(String())
    repetitions = Column(String())
    image = Column(String())
    mobilityscore = Column(Integer())
    dexterityscore = Column(Integer())


def update_user_activity_level(id, activity_level):
    session = Session()
    user_data = session.query(User).get(id)
    if user_data is not None:
        user_data.activity_level = activity_level
        session.commit()
        print(f"Updated user: {id} activity_level in DB successfully.")
    else:
        print(
            f"Not updating activity level for user: {id}, since user not found.")


def categorize_activity_level(activities):
    ACTIVITY_LEVELS = {
        'sedentary': ['watch_tv', 'study', 'eat', 'snack', 'read'],
        'low_active': ['personal_hygiene', 'bed_to_toilet', 'wakeup', 'shower', 'bed_toilet_transition', 'enter_home'],
        'active': ['work', 'wash_bathtub', 'wash_dishes' 'clean', 'cleaning', 'meal_preparation', 'cooking', 'cook', 'leave_home', 'gardening'],
        'very_active': ['exercise', 'run', 'jog', 'yoga', 'walk']
    }

    user_level_activity = {}

    level_of_activity = {
        'sedentary': 0,
        'low_active': 0,
        'active': 0,
        'very_active': 0
    }

    for user_id, user_activities in activities.items():
        level_of_activity = {
            'sedentary': 0,
            'low_active': 0,
            'active': 0,
            'very_active': 0
        }
        for user_activity, duration in user_activities.items():
            for level, activity in ACTIVITY_LEVELS.items():
                if (user_activity.lower() in activity):
                    level_of_activity[level] += duration

        user_level_activity[user_id] = level_of_activity

    # Find and update greatest level of activity for a user
    for user_id, user_level in user_level_activity.items():
        update_user_activity_level(
            id=user_id[1:], activity_level=max(user_level, key=user_level.get))


def load_history_adl_data():
    print(">>>> Loading ADL data the start of application.")

    # Convert txt file to csv, adding commas and removinh unwanted space
    with open(ADL_RAW_DATASET_LOCATION + 'data.txt', 'rt') as infile, open(ADL_RAW_DATASET_LOCATION + 'data.csv', 'w') as outfile:
        for line in infile:
            if re.search(r'\d+$', line.strip()):
                modified_line = line.strip() + ',\n'
            else:
                modified_line = line
            outfile.write(modified_line.replace('\t', ',').replace(
                ' ', '_').replace('ON\n', 'ON,\n').replace('OFF\n', 'OFF,\n'))
    infile.close()
    outfile.close()

    # Read CSV
    csv_file = pd.read_csv(
        ADL_RAW_DATASET_LOCATION + 'data.csv', header=None)

    # Adding header
    headerList = ['date', 'time', 'sensor_id', 'sensor_status', 'activity']

    csv_file.to_csv(ADL_RAW_DATASET_LOCATION + 'data.csv',
                    header=headerList, index=False)

    csv_file = pd.read_csv(ADL_RAW_DATASET_LOCATION + 'data.csv')

    # Feature engineering
    subset_file = csv_file.dropna()
    subset_file.drop(['sensor_id', 'sensor_status'], axis=1, inplace=True)
    subset_file['datetime'] = (
        subset_file['date'] + ' ' + subset_file['time'])
    subset_file.loc[subset_file['activity'].str.startswith(
        'R'), 'activity_name'] = subset_file['activity'].str.split('_', n=1, expand=True)[1]
    subset_file.loc[~subset_file['activity'].str.startswith(
        'R'), 'activity_name'] = subset_file['activity']

    subset_file.loc[subset_file['activity'].str.startswith(
        'R'), 'user_id'] = subset_file['activity'].str.split('_', n=1, expand=True)[0]
    subset_file.loc[~subset_file['activity'].str.startswith(
        'R'), 'user_id'] = 'ALL'

    subset_file['activity_name'] = subset_file['activity_name'].replace(
        "_begin", "", regex=True)
    subset_file['activity_name'] = subset_file['activity_name'].replace(
        "_end", "", regex=True)

    subset_file.to_csv(ADL_CSV_DATASET_LOCATION +
                       'data-cleaned.csv', index=False)

    ongoing_activities = {}
    activity_tracking = {}
    user_ids = subset_file['user_id'].drop_duplicates().values

    # Calculate amount of time (in min) spent for each activity by each user
    for id in user_ids:
        ongoing_activities[id] = {}
        activity_tracking[id] = {}

    for index, row in subset_file.iterrows():
        activity = row['activity']
        activity_name = row['activity_name']
        user_id = row['user_id']
        time = datetime.strptime(row['datetime'], "%Y-%m-%d %H:%M:%S.%f")

        if activity.endswith('begin'):
            ongoing_activities[user_id][activity_name] = time
            if activity_name not in activity_tracking[user_id]:
                activity_tracking[user_id][activity_name] = 0  # mins

        elif activity.endswith('end'):
            begin_timestamp = ongoing_activities[user_id][activity_name]
            if begin_timestamp:
                time_spent = time - begin_timestamp
                activity_tracking[user_id][activity_name] += time_spent.total_seconds()/60

    # Normalise time spent per activity per day by each user
    # Find start and end date
    start = datetime.strptime(
        subset_file.iloc[0]['datetime'], "%Y-%m-%d %H:%M:%S.%f")
    end = datetime.strptime(
        subset_file.iloc[-1]['datetime'], "%Y-%m-%d %H:%M:%S.%f")

    total_days = (end - start).days

    combined_activities = activity_tracking['ALL']

    for user_id, activities in activity_tracking.items():
        activity_tracking[user_id].update(combined_activities)
        for activity, duration in activities.items():
            activity_tracking[user_id][activity] = round(
                duration/total_days)

    activity_tracking.pop('ALL')

    # Reverse sort activities
    sorted_activities = {key: dict(sorted(value.items(), reverse=True, key=lambda element: element[1]))
                         for key, value in activity_tracking.items()}

    categorize_activity_level(activities=sorted_activities)


def activity_object(row):
    return Activity(**row)


def import_activity_csv_data(csv_file):
    print("Importing activity data.")
    # Connect to the activity db
    engine = create_engine(
        "sqlite:///" + os.path.join(BASE_DIRECTORY, 'activity.db'), echo=True)
    Base = declarative_base()
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    session = Session()
    print('Checking for any previous records:')
    existing_data = session.query(Activity).first()
    if existing_data is None:
        import_data = True
    else:
        import_data = False

    print(f'Import data?: {import_data}')

    if (import_data):
        with open(csv_file, encoding='utf-8', newline='') as file:
            # open and read csv
            csvreader = csv.DictReader(file, quotechar='"')

            # Create food object for every row in the csv
            activities = [activity_object(row) for row in csvreader]

            # Write to the food database, under food table
            session.add_all(activities)
            session.commit()
