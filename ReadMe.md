movie_recommendation is a local website where you can enter and rate some movies that you have already seen. Then you can choose between 2 modes(Explorer/Simular). Based on the movies and the mode you selected on the website, some movies are recommended for you.
In data_into_sql.py a Kaggle data set is uploaded from the hard drive to a local SQL server. The dataset contains Netflix films that have been rated by users.
functions.py contains all the necessary functions.
interface.py is the webside where you can enter and rate the movies you already know. By selecting a mode you choose between two different ways to get your recommendation.
Your entries don't have to be exact. The program finds the title even with spelling mistakes.
Modes:
    - Explorer: You will be given a random recommendation that excludes the listing you made, and the      movies have an average rating of at least 2.5
    - Simular: You will get a recommendation based on the reviews of other users. Your input will be accepted and appended to the existing ratings of the other users. The extended table is used to create a user_user_matrix (spearman correlation). Users with the highest simularity will be used and a recommendation will be calculated based on this.
After confirming your entry, you will receive 5 recommendations

data_into_sql.py:
  - read in data
  - upload to sql db

functions.py:
   - functions

interface.py:
  - interface of the webside with flask
  - random recommendation
  - user_user recommendation

templates:
  - html websides 

static:
  - styles.css
  - picture

data source: 
   - kaggle 

screenshots:
