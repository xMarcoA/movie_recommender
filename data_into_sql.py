import pandas as pd
from sqlalchemy import create_engine

# # read in data and preparation

ratings = pd.read_csv("../data/ml-latest-small/ratings.csv")
ratings = ratings.rename(columns = {'movieId': 'movieid','userId':'userid'})
movies = pd.read_csv("../data/ml-latest-small/movies.csv") 
movies = movies.rename(columns = {'movieId': 'movieid'})

movies_ratings = pd.merge(left=movies, right=ratings, how='left', on='movieid')

short = movies_ratings.drop(columns=['genres', 'timestamp', 'title'] ,axis=1)
user_item_matrix = short.pivot(index='movieid', columns='userid', values='rating')

# # upload sql

uri = f'postgres://localhost/movie_recommendation'
engine = create_engine(uri, echo=False)

movies.to_sql('movies', engine)
ratings.to_sql('ratings', engine)
movies_ratings.to_sql('movies_ratings', engine)
user_item_matrix.to_sql('user_item_matrix', engine)

