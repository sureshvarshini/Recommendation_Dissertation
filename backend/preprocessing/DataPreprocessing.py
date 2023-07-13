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
    nutrition_data = pd.read_csv(dataset_location + 'nutrition.csv')

    # Select columns: name, calories, cholesterol, folic_acid, vitamin_c, vitamin_d, calcium, iron, protein, carbohydrate, fiber, sugars, fat
    subset_nutrition_data = nutrition_data[["name", "calories", "cholesterol", "folic_acid",
                                            "vitamin_c", "vitamin_d", "calcium", "iron", "protein", "carbohydrate", "fiber", "sugars", "fat"]]

    print('\nChecking if there are any null or nan values in the selected columns:')
    print(f"--------\nIs Null?\n--------\n",
          subset_nutrition_data.isnull().sum())
    print(f"--------\nIs NA?\n--------\n", subset_nutrition_data.isna().sum())
    # No nan or null values

    # Replace strings in columns
    subset_nutrition_data = subset_nutrition_data.replace(
        'mcg', '', regex=True)
    subset_nutrition_data = subset_nutrition_data.replace('mg', '', regex=True)
    subset_nutrition_data = subset_nutrition_data.replace('g', '', regex=True)
    subset_nutrition_data = subset_nutrition_data.replace('IU', '', regex=True)

    # Covert columns to float dtype
    subset_nutrition_data = subset_nutrition_data.astype({'cholesterol': 'float',
                                                          'folic_acid': 'float',
                                                          'vitamin_c': 'float',
                                                          'vitamin_d': 'float',
                                                          'calcium': 'float',
                                                          'iron': 'float',
                                                          'protein': 'float',
                                                          'carbohydrate': 'float',
                                                          'fiber': 'float',
                                                          'sugars': 'float',
                                                          'fat': 'float'})

    # Check the types of the column are float
    print(subset_nutrition_data.dtypes)

    print('Printing subset of cleaned data:\n')
    print(subset_nutrition_data.head())

    # Write the cleaned dataset to a new csv
    print('Writing cleaned data to a new csv:\n')
    output_file_path = current_working_directory + '\\preprocessing\\cleanedDatasets\\'
    subset_nutrition_data.to_csv(
        output_file_path + 'nutrition_cleaned.csv', index=False)


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
