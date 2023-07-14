import pandas as pd
import numpy as np
import requests
import urllib
from urllib.request import urlopen
from urllib.parse import urlencode
import webbrowser
from scipy.sparse.linalg import svds
from models.Model import Rating

activity_levels = {
    'sedentary': 1.4,
    'low_active': 1.56,
    'active': 1.8,
    'very_active': 2.1
}


def daily_calorie_intake(user):
    # change to get activity level from user object
    activity_factor = activity_levels.get('very_active')
    if (user.gender.lower() == "male"):
        calories_male = ((10 * user.weight) + (6.25 * user.height) -
                         (5 * user.age) + 5) * activity_factor
        return calories_male
    else:
        calories_female = ((10 * user.weight) +
                           (6.25 * user.height) - (5 * user.age) - 161) * activity_factor
        return calories_female


def extract_macro_nutrients(calories, user):
    if (user.gender.lower() == "male"):
        fiber = 30  # g
        vitamin_a = 900  # mcg
        vitamin_c = 90  # mg
        if (user.age > 70):
            calcium = 1200  # mg
            vitamin_d = 20  # mcg
        else:
            calcium = 1000  # mg
            vitamin_d = 15  # mcg
    else:  # For females
        fiber = 21  # g
        vitamin_a = 700  # mcg
        vitamin_c = 75  # mg
        calcium = 1200  # mg

        if (user.age > 70):
            vitamin_d = 20  # mcg
        else:
            vitamin_d = 15  # mcg

    # Carbs - g
    carbohydrates = (0.45 * calories) / 4

    # Fats - g
    fats = (0.3 * calories) / 9

    # Proteins - g
    proteins = (1.2 * user.weight)

    macro_nutrients = {
        'carbohydrates': carbohydrates,
        'fats': fats,
        'proteins': proteins,
        'fiber': fiber,
        'vitamin_a': vitamin_a,
        'vitamin_c': vitamin_c,
        'vitamin_d': vitamin_d,
        'calcium': calcium
    }

    return macro_nutrients

# def submit_form(user): - not working

#     payload = urlencode({
#         'Measurement Unit': 'Metric',
#         'Sex': 'Female',
#         'Age': 89,
#         'Height': 180,
#         'Weight': 70,
#         'Activity level': 'Sedentary',
#         'Pregnancy/Lactation status': 'Not Pregnant or Lactating'
#     })

#     url = 'https://www.nal.usda.gov/human-nutrition-and-food-safety/dri-calculator' + '?' + payload

#     web_response = urlopen(url)

#     print("----> WEB RESPONSE")
#     print(str(web_response.getcode()))
#     with open("results.html", "wb") as f:
#         f.write(web_response.read())
#     webbrowser.open("results.html")


def get_food_recommendations(id):
    ratings_df = pd.DataFrame(Rating.fetch_all_ratings())

    data_matrix = pd.pivot_table(
        ratings_df, index=['user_id'], columns='food_id', values="rating")
    data_matrix.fillna(0, inplace=True)
    data_matrix['user_index'] = np.arange(0, data_matrix.shape[0], 1)
    data_matrix.set_index(['user_index'], inplace=True)

    # Singular Value Decomposition
    U, sigma, Vt = svds(data_matrix.to_numpy(), k=50)
    sigma = np.diag(sigma)
    all_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt)

    # Predicted ratings
    preds_df = pd.DataFrame(all_user_predicted_ratings,
                            columns=data_matrix.columns)
    user_id_index = id - 1

    sorted_user_ratings = data_matrix.iloc[user_id_index].sort_values(
        ascending=False)
    sorted_user_predictions = preds_df.iloc[user_id_index].sort_values(
        ascending=False)

    temp = pd.concat([sorted_user_ratings, sorted_user_predictions], axis=1)
    temp.index.name = 'food_id'
    temp.columns = ['user_ratings', 'user_predictions']
    temp = temp.loc[temp.user_ratings == 0]
    temp = temp.sort_values('user_predictions', ascending=False)
    recommendations = temp.head(5)
    similar_food_ids = list(recommendations.index.values)

    return similar_food_ids
