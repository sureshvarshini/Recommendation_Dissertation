from models.Model import User
import os
import re
import pandas as pd
import numpy as np
import warnings
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
warnings.filterwarnings("ignore")

BASE_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

ADL_RAW_DATASET_LOCATION = os.getcwd(
) + "\\preprocessing\\datasets\\Activity_predictor\\raw\\"

ADL_CSV_DATASET_LOCATION = os.getcwd() + "\\preprocessing\\cleanedDatasets\\ADL\\"

UPLOAD_FILE_LOCATION = os.getcwd(
) + "\\preprocessing\\datasets\\Activity_predictor\\request\\"

MORNING_ACTIVITIES = ['walking', 'exercise', 'hobbies']
EVENING_ACTIVITIES = ['reading', 'gardening', 'yoga']


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
        User.update_activity(id=user_id[1:], activity_level=max(
            user_level, key=user_level.get))


def append_data(file):
    with open(ADL_RAW_DATASET_LOCATION + 'data.txt', 'a') as data_file:
        data_file.write(file.read().decode() + '\n')
    data_file.close()


def clean_adl_data(file_name):
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
                       'data-cleaned.csv', mode='a', index=False, header=False)
    subset_file.to_csv(UPLOAD_FILE_LOCATION + 'data-temp.csv', index=False)

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
            # Divide by total days if incoming dataset contains data for more than 30 days
            if total_days != 0:
                activity_tracking[user_id][activity] = round(
                    duration/total_days)
            else:
                activity_tracking[user_id][activity] = round(
                    duration)
    activity_tracking.pop('ALL')

    # Reverse sort activities
    sorted_activities = {key: dict(sorted(value.items(), reverse=True, key=lambda element: element[1]))
                         for key, value in activity_tracking.items()}

    categorize_activity_level(activities=sorted_activities)
    analyse_meal_times(
        csv_file_location=UPLOAD_FILE_LOCATION + 'data-temp.csv')


def analyse_meal_times(csv_file_location):
    csv_file = pd.read_csv(csv_file_location)
    csv_file['datetime'] = pd.to_datetime(csv_file['datetime'])
    csv_file['hour'] = csv_file['datetime'].dt.hour
    csv_file['minute'] = csv_file['datetime'].dt.minute
    user_ids = csv_file['user_id'].unique()

    encoder = LabelEncoder()
    csv_file['activity_name'] = encoder.fit_transform(
        csv_file['activity_name'])
    csv_file['user_id'] = encoder.fit_transform(csv_file['user_id'])

    X = csv_file[['hour', 'minute', 'activity_name', 'user_id']]

    kmeans = KMeans(n_clusters=3, random_state=42)
    csv_file['cluster'] = kmeans.fit_predict(X)

    time_slots = [7, 8, 10, 12, 14, 16, 18, 20, 21, 22]

    # Initialize an empty dictionary to store the recommended meal times for each cluster and time slot
    meal_times_recommendations = {}

    # Group the data by cluster and time slot and calculate the mean hour for each group
    for cluster_id in range(3):
        cluster_data = csv_file[csv_file['cluster'] == cluster_id]
        cluster_recommendations = []

        for i in range(len(time_slots) - 1):
            start_time = time_slots[i]
            end_time = time_slots[i + 1]

            # Get the mean hour for the current time slot in the cluster
            mean_hour = cluster_data[(cluster_data['hour'] >= start_time) & (
                cluster_data['hour'] < end_time)]['hour'].mean()
            cluster_recommendations.append(mean_hour)

        meal_times_recommendations[f'Cluster {cluster_id + 1}'] = cluster_recommendations

    # Convert the dictionary to a DataFrame for easier visualization
    recommendations_df = pd.DataFrame(meal_times_recommendations)
    recommendations_df.index = ['Breakfast', 'Morning Activity 1', 'Morning Snacks', 'Morning Activity 2',
                                'Lunch', 'Afternoon Activity', 'Afternoon Snacks', 'Evening Activity', 'Dinner']

    user_schedule = {
        'Breakfast': 7,
        'Morning Activity 1': 8,
        'Morning Snacks': 10,
        'Morning Activity 2': 11,
        'Lunch': 13,
        'Afternoon Activity': 14,
        'Afternoon Snacks': 16,
        'Evening Activity': 17,
        'Dinner': 19
    }

    for index, row in recommendations_df.iterrows():
        n = 0
        if np.isnan(row['Cluster 1']):
            cluster_1 = 0
        else:
            cluster_1 = row['Cluster 1']
            n = n + 1
        if np.isnan(row['Cluster 2']):
            cluster_2 = 0
        else:
            cluster_2 = row['Cluster 2']
            n = n + 1
        if np.isnan(row['Cluster 3']):
            cluster_3 = 0
        else:
            cluster_3 = row['Cluster 3']
            n = n + 1

        user_schedule[row.name] = user_schedule[row.name] if n is 0 else round((cluster_1 + cluster_2 + cluster_3)/n)

    # Update user schedule in profile db
    for id in user_ids:
        if id != 'ALL':
            print(id[1:])
            User.update_schedule(id=id[1:], schedule=user_schedule)

