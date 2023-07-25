from models.Model import User
import os
import re
import pandas as pd
import warnings
from datetime import datetime
warnings.filterwarnings("ignore")

BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

ADL_RAW_DATASET_LOCATION = os.getcwd(
) + "\\preprocessing\\datasets\\Activity_predictor\\raw\\"

ADL_CSV_DATASET_LOCATION = os.getcwd() + "\\preprocessing\\cleanedDatasets\\ADL\\"

UPLOAD_FILE_LOCATION = os.getcwd(
) + "\\preprocessing\\datasets\\Activity_predictor\\request\\"


def categorize_activity_level(activities):
    ACTIVITY_LEVELS = {
        'sedentary': ['watch_tv', 'study', 'eat', 'snack'],
        'low_active': ['personal_hygiene', 'bed_to_toilet', 'wakeup', 'shower', 'bed_toilet_transition', 'enter_home'],
        'active': ['work', 'wash_bathtub', 'clean', 'cleaning', 'meal_preparation', 'cooking', 'cook', 'leave_home'],
        'very_active': ['exercise', 'run', 'jog']
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
        User.update_activity(id=user_id[1:], activity_level=max(
            user_level, key=user_level.get))


def append_data(file):
    with open(ADL_RAW_DATASET_LOCATION + 'data.txt', 'a') as data_file:
        data_file.write(file.read().decode() + '\n')
    data_file.close()


def clean_adl_data(file_name):
    print(">>>> Cleaning incoming ADL data.")

    # Convert txt file to csv, adding commas and removinh unwanted space
    with open(UPLOAD_FILE_LOCATION + file_name, 'rt') as infile, open(ADL_RAW_DATASET_LOCATION + 'data.csv', 'w') as outfile:
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
    headerList = ['datetime', 'sensor_id', 'sensor_status', 'activity']

    csv_file.to_csv(ADL_RAW_DATASET_LOCATION + 'data.csv',
                    header=headerList, index=False)

    csv_file = pd.read_csv(ADL_RAW_DATASET_LOCATION + 'data.csv')
    csv_file['datetime'] = csv_file['datetime'].str.replace('_', ' ')

    # Feature engineering
    subset_file = csv_file.dropna()
    subset_file.drop(['sensor_id', 'sensor_status'], axis=1, inplace=True)
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
