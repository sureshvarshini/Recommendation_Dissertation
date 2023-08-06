import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
from pulp import LpVariable, LpProblem, LpMinimize, lpSum, LpStatus
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

ACTIVITY_LEVELS = {
    'sedentary': 1.2,
    'low_active': 1.4,
    'active': 1.6,
    'very_active': 1.9
}

MEAL_TYPES = ['Breakfast', 'Morning Snack',
              'Lunch', 'Afternoon Snack', 'Dinner']

MEAL_PERCENTAGES = {'Breakfast': 0.15, 'Morning Snack': 0.10,
                    'Lunch': 0.35, 'Afternoon Snack': 0.10, 'Dinner': 0.30}

N_CLUSTERS = 10


def daily_calorie_intake(user):
    if user.activity_level is not None:
        activity_factor = ACTIVITY_LEVELS.get(user.activity_level)
    else:
        activity_factor = ACTIVITY_LEVELS.get('low_active')
    if (user.gender.lower() == "male"):
        calories_male = ((10 * user.weight) + (6.25 * user.height) -
                         (5 * user.age) + 5) * activity_factor
        return round(calories_male)
    else:
        calories_female = ((10 * user.weight) +
                           (6.25 * user.height) - (5 * user.age) - 161) * activity_factor
        return round(calories_female)


def extract_macro_nutrients(calories, user):
    if (user.gender.lower() == "male"):
        fiber = 30  # g
        vitamin_a = 900  # mcg
        vitamin_c = 90  # mg
        sugar = 36  # g
        if (user.age > 70):
            calcium_lower = 1200  # mg
            vitamin_d_lower = 20  # mcg
        else:
            calcium_lower = 1000  # mg
            vitamin_d_lower = 15  # mcg
        calcium_upper = 2000  # mg

    else:  # For females
        fiber = 21  # g
        vitamin_a = 700  # mcg
        vitamin_c = 75  # mg
        calcium_lower = 1200  # mg
        calcium_upper = 2000  # mg
        sugar = 25  # g

        if (user.age > 70):
            vitamin_d_lower = 20  # mcg
        else:
            vitamin_d_lower = 15  # mcg

    vitamin_d_upper = 100  # mcg
    folate = 400  # mcg

    # Carbs - g
    carbohydrates_lower = (0.45 * calories) / 4
    carbohydrates_upper = (0.65 * calories) / 4

    # Fats - g
    fats_lower = (0.2 * calories) / 9
    fats_upper = (0.35 * calories) / 9

    # Proteins - g
    proteins_lower = (1.0 * user.weight)
    proteins_upper = (1.5 * user.weight)

    macro_nutrients = {}
    for meal in MEAL_TYPES:
        percentage = MEAL_PERCENTAGES[meal]
        nutrient_split = {
            'calories': round(calories * percentage),
            'carbohydrates_lower': round(carbohydrates_lower * percentage),
            'carbohydrates_upper': round(carbohydrates_upper * percentage),
            'fats_lower': round(fats_lower * percentage),
            'fats_upper': round(fats_upper * percentage),
            'proteins_lower': round(proteins_lower * percentage),
            'proteins_upper': round(proteins_upper * percentage),
            'fiber': round(fiber * percentage),
            'vitamin_a': round(vitamin_a * percentage),
            'vitamin_c': round(vitamin_c * percentage),
            'vitamin_d_lower': round(vitamin_d_lower * percentage),
            'vitamin_d_upper': round(vitamin_d_upper * percentage),
            'calcium_lower': round(calcium_lower * percentage),
            'calcium_upper': round(calcium_upper * percentage),
            'folate': round(folate * percentage),
            'sugar': round(sugar * percentage)
        }
        macro_nutrients[meal] = nutrient_split

    return macro_nutrients


def choose_foods(macro_nutrients_ratio, foods_df):
    # Choose random foods seperated by meal type
    final_food_choices = []
    weekly_menu = prepare_weekly_menu(foods=foods_df)

    for meal in MEAL_TYPES:
        print(f'Constructing food model for meal: {meal}')
        print("--------------------------------------------")

        if (meal == 'Breakfast'):
            day_menu = weekly_menu[weekly_menu['type'] == 'Breakfast']
        elif (meal == 'Morning Snack'):
            day_menu = weekly_menu[(weekly_menu['type'] == 'Sandwiches') |
                                   (weekly_menu['type'] == 'Snacks')]
        elif (meal == 'Lunch'):
            day_menu = weekly_menu[(weekly_menu['type'] == 'Main') |
                                   (weekly_menu['type'] == 'Appetizers')]
        elif (meal == 'Afternoon Snack'):
            day_menu = weekly_menu[(weekly_menu['type'] == 'Beverages') |
                                   (weekly_menu['type'] == 'Breads') |
                                   (weekly_menu['type'] == 'Salads') |
                                   (weekly_menu['type'] == 'Dressins')]
        elif (meal == 'Dinner'):
            day_menu = weekly_menu[(weekly_menu['type'] == 'Main') |
                                   (weekly_menu['type'] == 'Desserts')]

        # Creating list for all food items present in DB
        all_food_ids = list(day_menu['id'])
        all_calories = dict(zip(all_food_ids, day_menu['calories']))
        all_carbohydrates = dict(
            zip(all_food_ids, day_menu['carbohydrates']))
        all_fats = dict(zip(all_food_ids, day_menu['fat']))
        all_proteins = dict(zip(all_food_ids, day_menu['protein']))
        all_fibers = dict(zip(all_food_ids, day_menu['fiber']))
        all_vitamin_a = dict(zip(all_food_ids, day_menu['vitamin_a']))
        all_vitamin_c = dict(zip(all_food_ids, day_menu['vitamin_c']))
        all_vitamin_d = dict(zip(all_food_ids, day_menu['vitamin_d']))
        all_calcium = dict(zip(all_food_ids, day_menu['calcium']))
        all_folate = dict(zip(all_food_ids, day_menu['folate']))
        all_sugars = dict(zip(all_food_ids, day_menu['sugars']))

        # Define objective sense - minimize fat intake
        problem = LpProblem(name='fats', sense=LpMinimize)

        # Declare variables for each menu item
        equation_variables = LpVariable.dicts(
            name='id', indices=all_food_ids, lowBound=0, cat='Continuous')

        # Objective statement - calculate calories
        problem += lpSum([day_menu.loc[day_menu['id'] == f, 'calories'].values[0]
                          * equation_variables[f] for f in all_food_ids]), "Objective"

        # Calorie constraints
        problem += lpSum([all_calories[f] * equation_variables[f] for f in all_food_ids]
                         ) <= macro_nutrients_ratio[meal]['calories'], "Calories"

        # Carbohydrate constraints
        problem += lpSum([all_carbohydrates[f] * equation_variables[f] for f in all_food_ids]
                         ) >= macro_nutrients_ratio[meal]['carbohydrates_lower'], "CarbohydratesMinimum"
        problem += lpSum([all_carbohydrates[f] * equation_variables[f] for f in all_food_ids]
                         ) <= macro_nutrients_ratio[meal]['carbohydrates_upper'], "CarbohydratesMaximum"

        # Fat constraints
        problem += lpSum([all_fats[f] * equation_variables[f] for f in all_food_ids]
                         ) >= macro_nutrients_ratio[meal]['fats_lower'], "FatsMinimum"
        problem += lpSum([all_fats[f] * equation_variables[f] for f in all_food_ids]
                         ) <= macro_nutrients_ratio[meal]['fats_upper'], "FatsMaximum"

        # Proteins constraints
        problem += lpSum([all_proteins[f] * equation_variables[f] for f in all_food_ids]
                         ) >= macro_nutrients_ratio[meal]['proteins_lower'], "ProteinsMinimum"
        problem += lpSum([all_proteins[f] * equation_variables[f] for f in all_food_ids]
                         ) <= macro_nutrients_ratio[meal]['proteins_upper'], "ProteinsMaximum"

        # Fiber constraints
        problem += lpSum([all_fibers[f] * equation_variables[f]
                          for f in all_food_ids]) <= macro_nutrients_ratio[meal]['fiber'], "Fiber"

        # Vitamin_A constraints
        problem += lpSum([all_vitamin_a[f] * equation_variables[f]
                          for f in all_food_ids]) <= macro_nutrients_ratio[meal]['vitamin_a'], "VitaminA"

        # Vitamin_C constraints
        problem += lpSum([all_vitamin_c[f] * equation_variables[f]
                          for f in all_food_ids]) <= macro_nutrients_ratio[meal]['vitamin_c'], "VitaminC"

        # Vitamin_D constraints
        problem += lpSum([all_vitamin_d[f] * equation_variables[f] for f in all_food_ids]
                         ) >= macro_nutrients_ratio[meal]['vitamin_d_lower'], "VitaminDMinimum"
        problem += lpSum([all_vitamin_d[f] * equation_variables[f] for f in all_food_ids]
                         ) <= macro_nutrients_ratio[meal]['vitamin_d_upper'], "VitaminDMaximum"

        # Calcium constraints
        problem += lpSum([all_calcium[f] * equation_variables[f] for f in all_food_ids]
                         ) >= macro_nutrients_ratio[meal]['calcium_lower'], "CalciumMinimum"
        problem += lpSum([all_calcium[f] * equation_variables[f] for f in all_food_ids]
                         ) <= macro_nutrients_ratio[meal]['calcium_upper'], "CalciumMaximum"

        # Folate constraints
        problem += lpSum([all_folate[f] * equation_variables[f]
                          for f in all_food_ids]) <= macro_nutrients_ratio[meal]['folate'], "Folate"

        # Sugar constraints
        problem += lpSum([all_sugars[f] * equation_variables[f]
                          for f in all_food_ids]) <= macro_nutrients_ratio[meal]['sugar'], "Sugar"

        # Solve the equation
        status = problem.solve()
        print("Problem Status:", LpStatus[status])  # expected - Optimal

        recommended_foods = {}
        for v in problem.variables():
            if v.varValue > 0:
                food_id = int(str(v.name).replace('id_', ''))
                recommended_foods[food_id] = v.varValue * 100
        final_food_choices.append(recommended_foods)
    return dict(zip(MEAL_TYPES, final_food_choices))


def prepare_weekly_menu(foods):
    # Shuffling the dataset for variety of options
    shuffled_food_data = foods.sample(
        frac=1).reset_index().drop('index', axis=1)

    return shuffled_food_data.sample(n=800)


def get_similar_users_recommendations(user_id, ratings, users):
    # Get top 3 foods with highest rating from top 3 similar users
    users_df = pd.DataFrame(users)
    ratings_df = pd.DataFrame(ratings)

    # Choosing similar users by features: age, weight, illness
    users_df_copy = users_df[['age', 'weight', 'illness']]
    # Label encoding the features
    encoder = LabelEncoder()
    # users_df_copy['age'] = encoder.fit_transform(users_df_copy['age'])
    # users_df_copy['weight'] = encoder.fit_transform(users_df_copy['weight'])
    users_df_copy['illness'] = encoder.fit_transform(users_df_copy['illness'])
    data_scalar = StandardScaler().fit_transform(users_df_copy)

    # KMeans clustering
    kmeans = KMeans(n_clusters=N_CLUSTERS, random_state=24)
    cluster_labels = kmeans.fit_predict(data_scalar)
    users_df_copy['cluster'] = cluster_labels

    user_cluster = users_df_copy.loc[users_df['id']
                                     == user_id, 'cluster'].iloc[0]
    similar_users = (users_df_copy[users_df_copy['cluster'] ==
                     user_cluster]).nlargest(10, 'illness')
    similar_users = similar_users[similar_users.index !=
                                  users_df.index[users_df['id'] == user_id].tolist()[0]]

    rated_food_ids = []
    for similar_user_id in similar_users.index:
        user_ratings = ratings_df[ratings_df['user_id'] == similar_user_id]
        top_rated_foods_df = user_ratings.nlargest(3, 'rating')
        for each_id in top_rated_foods_df['food_id'].tolist():
            if each_id not in rated_food_ids:
                rated_food_ids.append(each_id)
    return rated_food_ids


def get_similar_foods_recommendation(food_id, foods_df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(foods_df['type'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    food_index = pd.Series(
        foods_df.index, index=foods_df['id']).drop_duplicates()[food_id]

    similarity_scores = list(enumerate(cosine_sim[food_index]))
    similarity_scores = sorted(
        similarity_scores, key=lambda x: x[1], reverse=True)

    # Get top 5 similar foods
    similarity_scores = similarity_scores[1:6]
    food_indices = [i[0] for i in similarity_scores]
    return food_indices


def get_hybrid_recommendation(similar_users_recommendation_food_ids, foods, chosen_food_id):
    hybrid_recommendation = []
    for food_id in similar_users_recommendation_food_ids:
        id = get_similar_foods_recommendation(food_id, foods)
        if id not in hybrid_recommendation and chosen_food_id not in hybrid_recommendation:
            hybrid_recommendation.extend(id)

    return list(set(hybrid_recommendation))
