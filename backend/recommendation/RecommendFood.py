import pandas as pd
import numpy as np
from pulp import LpVariable, LpProblem, LpMaximize, lpSum, LpStatus
from scipy.sparse.linalg import svds

activity_levels = {
    'sedentary': 1.2,
    'low_active': 1.4,
    'active': 1.6,
    'very_active': 1.9
}

meal_types = ['Breakfast', 'Morning Snack',
              'Lunch', 'Afternoon Snack', 'Dinner']

meal_percentages = {'Breakfast': 0.15, 'Morning Snack': 0.10,
                    'Lunch': 0.35, 'Afternoon Snack': 0.10, 'Dinner': 0.30}


def daily_calorie_intake(user):
    # TODO: change to get activity level from user object
    activity_factor = activity_levels.get('sedentary')
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
    for meal in meal_types:
        percentage = meal_percentages[meal]
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
            'folate': round(folate * percentage)
        }
        macro_nutrients[meal] = nutrient_split

    return macro_nutrients


def choose_foods(macro_nutrients_ratio, foods):
    foods_df = pd.DataFrame(foods)

    # Choose random foods seperated by meal type
    final_food_choices = []
    weekly_menu = prepare_weekly_menu(foods=foods_df)

    for meal in meal_types:
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

        # Define objective sense - minimize fat intake
        problem = LpProblem(name='fats', sense=LpMaximize)

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

        # Solve the equation
        status = problem.solve()
        print("Problem Status:", LpStatus[status])  # expected - Optimal

        recommended_foods = {}
        for v in problem.variables():
            if v.varValue > 0:
                food_id = int(str(v.name).replace('id_', ''))
                recommended_foods[food_id] = v.varValue * 100
        final_food_choices.append(recommended_foods)
    return dict(zip(meal_types, final_food_choices))


def prepare_weekly_menu(foods):
    # Shuffling the dataset for variety of options
    shuffled_food_data = foods.sample(
        frac=1).reset_index().drop('index', axis=1)

    return shuffled_food_data.sample(n=800)


def get_food_recommendations(id, ratings):
    # This function returns the top 5 foods rated high by the user
    ratings_df = pd.DataFrame(ratings)

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
