#!/bin/python
from movielens import *
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans
from operator import itemgetter
import sys
import pickle

#hyperparameters:
cluster_num=19
TOP_N=150

# Store data in arrays
user = []
item = []
rating = []
rating_test = []

# Load the movie lens dataset into arrays
d = Dataset()
d.load_users("data/u.user", user)
d.load_items("data/u.item", item)
d.load_ratings("data/u.base", rating)
d.load_ratings("data/u.test", rating_test)

n_users = len(user)
n_items = len(item)

# The utility matrix stores the rating for each user-item pair in the matrix form.
# Note that the movielens data is indexed starting from 1 (instead of 0).
utility = np.zeros((n_users, n_items))
for r in rating:
    utility[r.user_id-1][r.item_id-1] = r.rating

test=np.zeros(shape=(n_users, n_items))
for r in rating_test:
    test[r.user_id -1][r.item_id-1]=r.rating

# Perform clustering on items

movie_genre = []
for movie in item:
    movie_genre.append([movie.unknown, movie.action, movie.adventure, movie.animation, movie.childrens, movie.comedy,
                        movie.crime, movie.documentary, movie.drama, movie.fantasy, movie.film_noir, movie.horror,
                        movie.musical, movie.mystery, movie.romance, movie.sci_fi, movie.thriller, movie.war, movie.western])
movie_genre = np.array(movie_genre)
cluster=KMeans(n_clusters=cluster_num)
cluster.fit_predict(movie_genre)

# Finds the average rating for each user and stores it in the user's object
for i in range(n_users):
    rated = np.nonzero(utility[i])
    n = len(rated[0])
    if n != 0:
        user[i].avg_r = np.mean(utility[i][rated])
    else:
        user[i].avg_r = 0.
print(utility)

#finish utility matrix for clustered ratings
mapping=cluster.labels_ # mapping between original categoy to our clustered categories
utility_clustered = np.zeros(shape=(n_users, cluster_num))
utility_clustered_num=np.zeros(shape=(n_users, cluster_num))
for i in range(n_users):
    for j1 in range(n_items):
        if utility[i][j1]>0:
            utility_clustered[i][ mapping[j1] ]+=utility[i][j1]
            utility_clustered_num[i][ mapping[j1] ]+=1
    for j2 in range(cluster_num):
        if utility_clustered[i][j2]>0:
            utility_clustered[i][j2] /=utility_clustered_num[i][j2] # average rating for each clustered category   


similarity=np.zeros(shape=(n_users, n_users))
# Finds the Pearson Correlation Similarity Measure between two users
def pcs(x, y): # I should implement a weighted pcs next time


    #userx=user[x-1]
    #usery=user[y-1]

    if similarity[x-1][y-1] is not None:
        return
 
    common_index=[i for i,e in enumerate(utility_clustered[x-1]) if e!=0 and utility_clustered[y-1][i]!=0]
    if not common_index:  # there's no common index 
        similarity[x-1][y-1]=0
        print("No film under common categories for user{} and user{}".format(x, y))
        return
    ratingx=[utility_clustered[x-1][each] for each in common_index]
    ratingy=[utility_clustered[y-1][each] for each in common_index]
    x_avg=np.mean(ratingx)
    y_avg=np.mean(ratingy)

    ratingx-=x_avg  # I think this not the perfect answer 
    ratingy-=y_avg # weighted person coefficient is better
    similarity[x-1][y-1]=np.dot(ratingx, ratingy)/ (np.linalg.norm(ratingx)*np.linalg.norm(ratingy) )

  

# Guesses the ratings that user with id, user_id, might give to item with id, i_id.
# We will consider the top_n similar users to do this.
def guess(user_id, i_id, top_n=TOP_N):

 
    distance=[ (id+1,e) for id,e in enumerate(similarity[user_id-1]) if (id+1)!=user_id ]  #(i,e)-> (User_y_id-1, pcs(x,y))           
    distance.sort(key=itemgetter(1), reverse=True)
    distance=distance[:top_n]
    # rating_u=np.average( [utility[i-1][i_id-1]  for i in list( map(itemgetter(0) , distance)) ] )
    neighbour_index=[ i-1 for i in list( map(itemgetter(0) , distance) ) if utility_clustered[i-1][ mapping[i_id-1] ]!=0 ] #this time NO offset!!!
    weight=utility_clustered_num[neighbour_index, mapping[i_id-1] ]/sum(utility_clustered_num[neighbour_index, mapping[i_id-1] ] )
    neighbour_rating_normalized=np.array([ utility_clustered[i][i_id-1] -user[i-1].avg_r for i in neighbour_index ])
    rating_u=user[user_id-1].avg_r + \
             np.average(neighbour_rating_normalized, weights=weight)
    return rating_u



# Predict the ratings of the user-item pairs in rating_test
# Find mean-squared error

#We will first fill the similarity matrix first
for i in range(n_users):
    for j in range(n_users):
        if j!=i:
            if similarity[j][i]>0:
                similarity[i][j]=similarity[j][i]
            else:
                pcs(i+1, j+1)    


#predicti
utility_copy = np.copy(utility_clustered)
for i in range(0, n_users):
    for j in range(0, cluster_num):
        if utility_copy[i][j] == 0:
            utility_copy[i][j] = guess(i+1, j+1)
y_true = []
y_pred = []
for i in range(0, n_users):
    for j in range(0, n_items):
        if test[i][j]>0:
            y_true.append(test[i][j])
            y_pred.append(utility_copy[i][ mapping[j] ])
print("Mean squared error={}".format(mean_squared_error(y_true, y_pred)))


#save our results
pickle.dump(utility_copy,  open("utility_matrix.pkl", "wb") )
with open("meta_info", "w") as f:
    f.write(str(TOP_N)+"\n") 
    f.write(str(cluster_num)+"\n") 
    for each in mapping:
        f.write( str(each)+"\n" )         