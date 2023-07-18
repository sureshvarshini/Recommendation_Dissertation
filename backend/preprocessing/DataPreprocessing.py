import numpy as np
import os
import pandas as pd


def clean_food_csv():
    print('Starting: Cleaning food csv')
    # Navigate to dataset directory
    current_working_directory = os.getcwd()

    # Set location to Datasets
    dataset_location = current_working_directory + \
        '\\preprocessing\\datasets\\Food_recommender\\'

    # Source Dataset location = D:\Varshini\CourseWork\Dissertation\Implementation\Recommendation_Dissertation\backend\preprocessing\datasets\Food_recommender\

    # Read the entire CSV
    food_data = pd.read_csv(dataset_location + 'food_data.csv')

    print('\nChecking if there are any null or nan values in the selected columns:')
    print(f"--------\nIs NA?\n--------\n", food_data.isna().sum())
    # No nan or null values

    # Replace strings in columns
    food_data = food_data.replace('mcg RAE', '', regex=True)
    food_data = food_data.replace('mcg DFE', '', regex=True)
    food_data = food_data.replace('mg', '', regex=True)
    food_data = food_data.replace('g', '', regex=True)
    food_data = food_data.replace('\'', '', regex=True)
    food_data = food_data.replace('\[', '', regex=True)
    food_data = food_data.replace('\]', '', regex=True)
    food_data = food_data.replace('mc', '', regex=True)
    food_data = food_data.replace('milliliter', '', regex=True)

    # Covert columns to float dtype
    food_data = food_data.astype({'cholesterol': 'float',
                                  'calories': 'float',
                                  'vitamin_a': 'float',
                                  'vitamin_c': 'float',
                                  'vitamin_d': 'float',
                                  'calcium': 'float',
                                  'iron': 'float',
                                  'protein': 'float',
                                  'carbohydrates': 'float',
                                  'fiber': 'float',
                                  'sugars': 'float',
                                  'fat': 'float',
                                  'folate': 'float'})

    # Check the types of the column are float
    print(food_data.dtypes)

    print('Printing subset of cleaned data:\n')
    print(food_data.head())

    # Write the cleaned dataset to a new csv
    print('Writing cleaned data to a new csv:\n')
    output_file_path = current_working_directory + \
        '\\preprocessing\\cleanedDatasets\\'
    food_data.to_csv(
        output_file_path + 'food_data_cleaned.csv', index=False)


def clean_rating_csv():
    print('Starting: Cleaning rating csv')
    # Navigate to dataset directory
    current_working_directory = os.getcwd()

    # Set location to Datasets
    dataset_location = current_working_directory + \
        '\\preprocessing\\datasets\\Food_recommender\\'

    # Source Dataset location = D:\Varshini\CourseWork\Dissertation\Implementation\Recommendation_Dissertation\backend\preprocessing\datasets\Food_recommender\

    # Read the entire CSV
    rating_data = pd.read_csv(dataset_location + 'ratings_small.csv')

    # Select columns: userId, movieId, rating
    subset_rating_data = rating_data[["userId", "movieId", "rating"]]

    print('\nChecking if there are any null or nan values in the selected columns:')
    print(f"--------\nIs Null?\n--------\n",
          subset_rating_data.isnull().sum())
    print(f"--------\nIs NA?\n--------\n", subset_rating_data.isna().sum())
    # No nan or null values

    # Covert columns to float dtype
    subset_rating_data = subset_rating_data.astype({'rating': 'int64'})

    # Modify column names to include the unit
    subset_rating_data.rename(columns={'userId': 'user_id',
                                       'movieId': 'food_id'}, inplace=True)

    # Check the types of the column are float
    print(subset_rating_data.dtypes)

    print('Printing subset of cleaned data:\n')
    print(subset_rating_data.head())

    # Write the cleaned dataset to a new csv
    print('Writing cleaned data to a new csv:\n')
    output_file_path = current_working_directory + \
        '\\preprocessing\\cleanedDatasets\\'
    subset_rating_data.to_csv(
        output_file_path + 'ratings_cleaned.csv', index=False)
