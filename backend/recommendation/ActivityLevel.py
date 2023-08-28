from models.Model import User
import os
import re
import pandas as pd
import numpy as np
from statistics import mean
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.utils import resample
from datetime import datetime
from ImportAdl import write_to_db
import warnings
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
    available_slots = {}
    user_adl_dataset = {'user_id': [],
                        'activity': [],
                        'start_datetime': [],
                        'end_datetime': [],
                        'duration': []
                        }
    user_ids = subset_file['user_id'].drop_duplicates().values

    # Calculate amount of time (in min) spent for each activity by each user
    for id in user_ids:
        ongoing_activities[id] = {}
        activity_tracking[id] = {}
        if (id != 'ALL'):
            available_slots[id] = []

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

                # Add it to user adl dict
                user_adl_dataset['user_id'].append(user_id)
                user_adl_dataset['activity'].append(activity_name)
                user_adl_dataset['start_datetime'].append(begin_timestamp)
                user_adl_dataset['end_datetime'].append(time)
                user_adl_dataset['duration'].append(round(time_spent.total_seconds()/60))

    print(user_adl_dataset)
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

    # Find activity level
    categorize_activity_level(activities=sorted_activities)
    # analyse_meal_times(csv_file_location=UPLOAD_FILE_LOCATION + 'data-temp.csv')

    # Find times when user is idle
    adl_df = pd.DataFrame(user_adl_dataset)
    user_ids = adl_df['user_id'].unique()
    all_rows = adl_df[adl_df['user_id'] == 'ALL']

    for id in user_ids:
        all_rows_temp = all_rows.copy()

        if(id != 'ALL'):
            print(f"Finding slots for: {id}")
            print("------------------------")
            slots = []

            all_rows_temp['user_id'] = id
            all_rows_temp.reset_index(drop=True, inplace=True)

            # Get user_id separate dfs
            user_df_temp = adl_df[adl_df['user_id'] == id]
            frames = [all_rows_temp, user_df_temp]
            user_df = pd.concat(frames)

            user_df.sort_values(by='start_datetime', inplace=True)
            user_df.reset_index(drop=True, inplace=True)
            user_df['time_diff'] = user_df['start_datetime'] - user_df['end_datetime'].shift(1)

            # Convert ALL to user_ids - duplicate the ALL rows
            for index, row in all_rows_temp.iterrows():
                # Add it to user adl dict
                user_adl_dataset['user_id'].append(id)
                user_adl_dataset['activity'].append(row['activity'])
                user_adl_dataset['start_datetime'].append(row['start_datetime'])
                user_adl_dataset['end_datetime'].append(row['end_datetime'])
                user_adl_dataset['duration'].append(row['duration'])

            threshold_gap = pd.Timedelta(minutes=30)

            # Find the periods of no activity
            no_activity_periods = user_df[user_df['time_diff'] > threshold_gap]

            for index, row in no_activity_periods.iterrows():
                if(row['activity'] != 'wakeup' and row['activity'] != 'sleep'):
                    print(f"No activity recorded between {user_df['start_datetime'].iloc[index - 1]} and {row['start_datetime']}")
                    slots.append((str(user_df['start_datetime'].iloc[index - 1]), str(row['start_datetime'])))

                    # Add it to user adl dictionary
                    difference =  datetime.strptime(str(row['start_datetime']), '%Y-%m-%d %H:%M:%S.%f') - datetime.strptime(str(user_df['start_datetime'].iloc[index - 1]), '%Y-%m-%d %H:%M:%S.%f')
                    user_adl_dataset['user_id'].append(id)
                    user_adl_dataset['activity'].append('No')
                    user_adl_dataset['start_datetime'].append(user_df['start_datetime'].iloc[index - 1])
                    user_adl_dataset['end_datetime'].append(row['start_datetime'])
                    user_adl_dataset['duration'].append(round(difference.total_seconds()/60))
            available_slots[id] = slots
            print()
    adl_df = pd.DataFrame(user_adl_dataset)
    # Drop rows with 'ALL' -- adl_df is final adl dataframe for user written into sql db
    adl_df = adl_df[adl_df['user_id'] != 'ALL']
    adl_df.reset_index(drop=True, inplace=True)
    adl_df['user_id'] = adl_df['user_id'].str.replace('R', '').astype(int)
    adl_df.to_csv(ADL_CSV_DATASET_LOCATION + 'data-user-cleaned.csv', mode='a', index=False, header=False)   
    print()

    # Write ADL of user to db
    write_to_db(csv_file = ADL_CSV_DATASET_LOCATION + 'data-user-cleaned.csv')


def analyse_free_times(user_adl_df, this_activity):   
    # Construct features for ML model
    # Get what day of week, starts from 0-6 (Monday, Tuesday, Sunday)
    user_adl_df['day'] = pd.to_datetime(
        user_adl_df['start_datetime']).dt.day_of_week
    # Returns the hour of the day
    user_adl_df['start_hour'] = pd.to_datetime(
        user_adl_df['start_datetime']).dt.hour
    user_adl_df['activity'] = [1 if activity in this_activity
                                else 0 for activity in user_adl_df['activity']]
    # print(user_adl_df)

    # Identify feature and target variables
    X = user_adl_df[['day', 'start_hour']]
    y = user_adl_df['activity']

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2)

    # Oversampling minority class in train data - only for finding leisure time
    if 'No' in this_activity:
        print("Oversmapling leisure activities time.\n")
        train_data = pd.concat([X_train, y_train], axis=1)
        majority_activity = train_data[train_data['activity'] == 0]
        minority_activity = train_data[train_data['activity'] == 1]

        minority_oversampled = resample(
            minority_activity, replace=True, n_samples=len(majority_activity), random_state=29)
        sampled_activities = pd.concat(
            [majority_activity, minority_oversampled])

        X_train_sampled = sampled_activities.drop('activity', axis=1)
        y_train_sampled = sampled_activities['activity']

        # Train model
        model = RandomForestClassifier()
        model.fit(X_train_sampled, y_train_sampled)
    else:
        print("No oversampling for meal times.\n")
        
        # Train model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))

    # Get current day, user's wakeup and sleep time
    day_of_week = datetime.now().weekday()
    wakeup_rows = user_adl_df[user_adl_df['activity'] == 'wakeup']
    sleep_rows = user_adl_df[user_adl_df['activity'] == 'sleep']
    wakeup_times = []
    sleep_times = []

    for _, row in wakeup_rows.iterrows():
        wakeup_times.append(datetime.strptime(
            str(row['start_datetime']), '%Y-%m-%d %H:%M:%S.%f').hour)

    for _, row in sleep_rows.iterrows():
        sleep_times.append(datetime.strptime(
            str(row['start_datetime']), '%Y-%m-%d %H:%M:%S.%f').hour)

    # Assign default wakeup and sleep time if no value present
    if (len(wakeup_times) != 0 and len(sleep_times) != 0):
        wakeup = round(mean(wakeup_times))
        sleep = round(mean(sleep_times) + 12)
    else:
        # Default wakeup and sleep time
        wakeup = 6
        sleep = 21

    today_data = pd.DataFrame(
        {'day': day_of_week, 'start_hour': np.arange(wakeup, sleep)})
    prediction = model.predict(today_data)

    print(prediction)
    free_time_slots = today_data[prediction == 1]

    return free_time_slots

def find_breakfast_time(user_adl_df):
    wakeup_rows = user_adl_df[user_adl_df['activity'] == 'wakeup']
    wakeup_times = []

    for _, row in wakeup_rows.iterrows():
        wakeup_times.append(datetime.strptime(
            str(row['start_datetime']), '%Y-%m-%d %H:%M:%S.%f').hour)

    # Assign default wakeup and sleep time if no value present
    if (len(wakeup_times) != 0):
        wakeup = round(mean(wakeup_times))
    else:
        # Default wakeup and sleep time
        wakeup = 6
    
    return wakeup + 1

def find_dinner_time(user_adl_df):
    sleep_rows = user_adl_df[user_adl_df['activity'] == 'sleep']
    sleep_times = []

    for _, row in sleep_rows.iterrows():
        sleep_times.append(datetime.strptime(
            str(row['start_datetime']), '%Y-%m-%d %H:%M:%S.%f').hour)

    # Assign default wakeup and sleep time if no value present
    if (len(sleep_times) != 0):
        sleep = round(mean(sleep_times) + 12)
    else:
        # Default sleep time
        sleep = 21
    
    return sleep - 2
