
#!/bin/python
import numpy as np
from sklearn.metrics import mean_squared_error
from operator import itemgetter
# User class stores the names and average rating for each user
class User:
    def __init__(self, name, user_id):
        self.name = name
        self.id = user_id
        self.avg_r = None

# Item class stores the name of each item
class Item:
    def __init__(self, name, item_id):
        self.name = name
        self.id = item_id

# Rating class is used to assign ratings
class Rating:
    def __init__(self, user_id, item_id, rating):
        self.user_id = user_id
        self.item_id = item_id
        self.rating = rating

# We store users in a list. Note that user IDs start indexed at 1.
user = []
user.append(User("Ann", 1))
user.append(User("Bob", 2))
user.append(User("Carl", 3))
user.append(User("Doug", 4))

# Items are also stored in a list. Note that item IDs start indexed at 1.
item = []
item.append(Item("HP1", 1))
item.append(Item("HP2", 2))
item.append(Item("HP3", 3))
item.append(Item("SW1", 4))
item.append(Item("SW2", 5))
item.append(Item("SW3", 6))

rating = []
rating.append(Rating(1, 1, 4))
rating.append(Rating(1, 4, 1))
rating.append(Rating(2, 1, 5))
rating.append(Rating(2, 2, 5))
rating.append(Rating(2, 3, 4))
rating.append(Rating(3, 4, 4))
rating.append(Rating(3, 5, 5))
rating.append(Rating(4, 2, 3))
rating.append(Rating(4, 6, 3))

n_users = len(user)
n_items = len(item)
n_ratings = len(rating)

# The utility matrix stores the rating for each user-item pair in the matrix form.
utility = np.zeros((n_users, n_items))
for r in rating:
    utility[r.user_id-1][r.item_id-1] = r.rating
similarity=np.zeros(shape=(len(utility), len(utility) ) )
similarity[:]=None



# Finds the Pearson Correlation Similarity Measure between two users
def pcs(x, y):


    #I assume x and y refer to the id 
    #avg score
    userx=user[x-1]
    usery=user[y-1]
    userx.avg_r=np.sum(utility[x-1])/np.count_nonzero(utility[x-1])  if userx.avg_r is None \
                else userx.avg_r
    usery.avg_r=np.sum(utility[y-1])/np.count_nonzero(utility[y-1])  if usery.avg_r is None \
                else usery.avg_r
    if similarity[x-1][y-1] is not None:
        return
 
    common_index=[i for i,e in enumerate(utility[x-1]) if e!=0 and utility[y-1][i]!=0]
    if not common_index:  # there's no common index 
        similarity[x-1][y-1]=0
        return
    ratingx=[utility[x-1][each] for each in common_index]
    ratingy=[utility[y-1][each] for each in common_index]
    
    ratingx-=userx.avg_r
    ratingy-=usery.avg_r
    similarity[x-1][y-1]=np.dot(ratingx, ratingy)/ (np.linalg.norm(ratingx)*np.linalg.norm(ratingy) )
    #return similarity[x-1][y-1]

# Guesses the ratings that user with id, user_id, might give to item with id, i_id.
# We will consider the top_n similar users to do this. Use top_n as 3 in this example.
def guess(user_id, i_id, top_n=3):
   
    for y in range( len(utility) ):
        if y+1==user_id:
            continue
        else:
            pcs(user_id, y+1)
    distance=[ (id+1,e) for id,e in enumerate(similarity[user_id-1]) if (id+1)!=user_id ]  #(i,e)-> (User_y_id-1, pcs(x,y))           
    distance.sort(key=itemgetter(1), reverse=True)
    distance=distance[:top_n]
    # rating_u=np.average( [utility[i-1][i_id-1]  for i in list( map(itemgetter(0) , distance)) ] )
    rating_u=user[user_id-1].avg_r + \
             np.average( [utility[i-1][i_id-1]-user[i-1].avg_r  for i in list( map(itemgetter(0) , distance) ) \
             if utility[i-1][i_id-1]!=0 ] )
    return rating_u



# Display the utility matrix as given in Part 1 of your project description
np.set_printoptions(precision=3)
print(utility)

# Finds the average rating for each user and stores it in the user's object


n = 3 # Assume top_n users

# Finds all the missing values of the utility matrix
utility_copy = np.copy(utility)
for i in range(n_users):
    for j in range(n_items):
        if utility_copy[i][j] == 0:
            utility_copy[i][j] = guess(i+1, j+1, n)

print(utility_copy)

# Finds the utility values of the particular users in the test set. Refer to Q2
print ("Ann's rating for SW2 should be " + str(guess(1, 5, n)) )
print ("Carl's rating for HP1 should be " + str(guess(3, 1, n)) )
print ("Carl's rating for HP2 should be " + str(guess(3, 2, n)) )
print ("Doug's rating for SW1 should be " + str(guess(4, 4, n)) )
print ("Doug's rating for SW2 should be " + str(guess(4, 5, n)) )

guesses = np.array([guess(1, 5, n), guess(3, 1, n), guess(3, 2, n), guess(4, 4, n), guess(4, 5, n)])

### Ratings from the test set
# Ann rates SW2 with 2 stars
# Carl rates HP1 with 2 stars
# Carl rates HP2 with 2 stars
# Doug rates SW1 with 4 stars
# Doug rates SW2 with 3 stars

test = np.array([2, 2, 2, 4, 3])

# Finds the mean squared error of the ratings with respect to the test set
print("Mean Squared Error is " + str(mean_squared_error(guesses, test)))