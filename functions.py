from fuzzywuzzy import process # why do i have to import it here?
import numpy as np
import pandas as pd

#
#   general functions
#

def title_into_movieId(user_input,  movie_matrix):    
    """ takes a list of titles and returns the corresponding movieIds in a list """

    return [process.extractOne(movie, movie_matrix['title'])[2] for movie in user_input]

def movieId_into_title(recomendations_id, movie_matrix): 
    """ takes a list of movieIds and returns the corresponding titles in a list """

    rec = movie_matrix.loc[recomendations_id,"title"]
    return list(rec.values)

#
#   recommandation functions
#

def random_recommendation(user_item, id_list, min_rating = 2.5, number_of_recommandations= 5): 
    """ returns a list of recomandation as id's """ 
    
    min_filter = user_item.transpose().count() >= 100
    rating_filter = user_item.loc[min_filter].transpose().mean() >= min_rating
    un_seen_movies = user_item.drop(id_list)
    clean = un_seen_movies.loc[min_filter].loc[rating_filter]    
    return clean.transpose().mean().sample(number_of_recommandations).index

def new_user_item(user_item, id_list, user_input): 
    """ appends the user input to the eisting user-item-matrix """
    
    all_movieIds = list(user_item.transpose().columns) 
    empty_list = [np.nan]*len(all_movieIds)
    ratings_dict = dict(zip(all_movieIds, empty_list))
    for i in id_list:
        for film, rating in user_input.items():
            ratings_dict[i] = rating
    user_vector = pd.DataFrame(list(ratings_dict.values()), index=all_movieIds, columns=['new'])
    return pd.concat([user_item.transpose(),user_vector.transpose()])

def simular_user_recommendation(new_user_item):
    """ 
    creates a user-user-matrix with the given matrix 
    and returns the best 5 recomandations as a list of movieIds 
    """
    
    user_user = new_user_item.transpose().corr(method="spearman")
    neighboors = user_user.loc['new']
    neighboors = neighboors.sort_values(ascending=False).iloc[1:6]
    unrated_items = new_user_item.loc['new'].isna()
    neighboors_ratings = new_user_item.loc[neighboors.index, unrated_items]
    min_filter = neighboors_ratings.transpose().count() >= 100
    clean = neighboors_ratings.loc[min_filter]
    recommandation = clean.mean().sort_values(ascending=False)
    return recommandation.dropna().iloc[:5].index


