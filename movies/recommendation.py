import os
from typing import List
import numpy as np
import pandas as pd
from pandas.core.common import flatten
from django.contrib.auth import get_user_model
from django.conf import settings
from .models import UserRating

DATA_FILE = 'data/ratings.csv'
path = os.path.join(settings.BASE_DIR, DATA_FILE)
rating = pd.read_csv(path)
movie = pd.read_csv(os.path.join(settings.BASE_DIR, 'data/movie_data.csv'), delimiter=';')
movie.drop(columns=['genres', 'year'], inplace=True)


def recommender(user: get_user_model()) -> List[str]:
    user_rating_obj_set = UserRating.objects.filter(user=user)
    rated_movies_by_user = [user_rating_obj.movie.title for user_rating_obj in user_rating_obj_set]
    ratings_by_user = [user_rating_obj.user_rating for user_rating_obj in user_rating_obj_set]
    movie_rating_data = list(zip(rated_movies_by_user, ratings_by_user))
    user_movie_rating_data = [{'title': _title, 'rating': _rating} for _title, _rating in movie_rating_data]
    input_movie = pd.DataFrame(user_movie_rating_data)
    # Filtering out the movies by title
    movie_id = movie.loc[movie['title'].isin(input_movie['title'].tolist())]
    input_movie = pd.merge(movie_id, input_movie)
    # Get users who watched the similar movies
    users = rating.loc[rating['movieId'].isin(input_movie['movieId'].tolist())]
    user_subset_group = users.groupby(['userId'])
    # Sort user_subset_group so that users who have similar movie taste will have higher priority
    user_subset_group = sorted(user_subset_group, key=lambda x: len(x[1]), reverse=True)[0:100]
    # Define Pearson Correlation dict
    pearson_cor_dict = {}
    for name, group in user_subset_group:
        group = group.sort_values(by='movieId')
        len_group = len(group)
        input_movie = input_movie.sort_values(by='movieId')

        # Review scores for the movies that they both have in common
        temp = input_movie.loc[input_movie['movieId'].isin(group['movieId'].tolist())]
        temp_rating_list = temp['rating'].tolist()
        temp_group_list = group['rating'].tolist()

        # Calculate the Pearson Correlation between two users
        s_xx = sum([i ** 2 for i in temp_rating_list]) - pow(sum(temp_rating_list), 2) / float(len_group)
        s_yy = sum([i ** 2 for i in temp_group_list]) - pow(sum(temp_group_list), 2) / float(len_group)
        s_xy = \
            sum(i * j for i, j in zip(temp_rating_list, temp_group_list)) \
            - sum(temp_rating_list) * sum(temp_group_list) / float(len_group)

        if s_xx != 0 and s_yy != 0:
            pearson_cor_dict[name] = s_xy / np.sqrt(s_xx * s_yy)
        # If the denominator is 0, correlation is 0.
        else:
            pearson_cor_dict[name] = 0

    pearson_df = pd.DataFrame.from_dict(pearson_cor_dict, orient='index')
    pearson_df.columns = ['similarityIndex']
    pearson_df['userId'] = pearson_df.index
    pearson_df.index = range(len(pearson_df))
    top_users = pearson_df.sort_values(by='similarityIndex', ascending=False)[0:50]
    top_users_rating = top_users.merge(rating, left_on='userId', right_on='userId', how='inner')
    # Multiply the similarity by the ratings of users
    top_users_rating['weightedRating'] = top_users_rating['similarityIndex'] * top_users_rating['rating']
    temp_top_users_rating = top_users_rating.groupby('movieId').sum()[['similarityIndex', 'weightedRating']]
    temp_top_users_rating.columns = ['sum_similarityIndex', 'sum_weightedRating']
    # Define recommendation_df dict
    recommendation_df = pd.DataFrame()
    # The weighted average
    recommendation_df['weighted average recommendation score'] = \
        temp_top_users_rating['sum_weightedRating'] / \
        temp_top_users_rating['sum_similarityIndex']

    recommendation_df['movieId'] = temp_top_users_rating.index
    recommendation_df = recommendation_df.sort_values(by='weighted average recommendation score', ascending=False)
    # Get the first 10 recommendations to be returned
    recommendation_list = movie.loc[movie['movieId'].isin(recommendation_df.head(10)['movieId'].tolist())]
    recommendation_list_new = recommendation_list.copy()
    recommendation_list_new.drop(columns=['movieId'], inplace=True)
    recommendation_list_new = recommendation_list_new.values.tolist()
    recommendation_list_new = list(flatten(recommendation_list_new))

    return recommendation_list_new
