# imports
    
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect, url_for
from fuzzywuzzy import process
from sqlalchemy import create_engine
from functions import random_recommendation
from functions import title_into_movieId
from functions import movieId_into_title
from functions import new_user_item
from functions import simular_user_recommendation

#
# read in data
#

uri = f'postgres://localhost/movie_recommendation'
engine = create_engine(uri, echo=False)

query_ui = "SELECT * FROM user_item_matrix;"
query_mm = "SELECT movieid, title FROM movies;"

user_item_matrix = pd.read_sql(query_ui, engine, index_col="movieid")
user_item_matrix = user_item_matrix.drop(axis=1,columns="nan")

movieID_title = pd.read_sql(query_mm, engine, index_col="movieid")

#
# flask object
#

app = Flask(__name__)

@app.route('/')
def index():
    print(request.args)
    return render_template('index.html')

@app.route('/movies/search')
def movie_search():
    


    movie_queries = [movie for movie in request.args.getlist('movie') if movie != ""]
    ratings = [float(rating) for rating in request.args.getlist('rating') if rating != ""]
    
    modes = request.args.get("modes")

    # {'title':'rating'}
    user_input_dict = dict(zip(movie_queries, ratings)) 
    print(user_input_dict)  
    if modes == "explore":
        ids = title_into_movieId(user_input_dict, movieID_title)
        recommendation_id = random_recommendation(user_item_matrix, ids)
        recommendation_title = movieId_into_title(recommendation_id,movieID_title)
    elif modes == "simular":
        ids = title_into_movieId(user_input_dict, movieID_title)
        new_user_item_matrix = new_user_item(user_item_matrix,ids, user_input_dict)
        recommendation_sim = simular_user_recommendation(new_user_item_matrix)
        recommendation_title = movieId_into_title(recommendation_sim,movieID_title)
    else:
        recommendation_title = ["Please select a mode"]
    return render_template('results.html', matches=recommendation_title)

if __name__ == "__main__":
    app.run(debug=True)

