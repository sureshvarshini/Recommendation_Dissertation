import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from scipy.sparse.linalg import svds
from models.Model import Rating


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
