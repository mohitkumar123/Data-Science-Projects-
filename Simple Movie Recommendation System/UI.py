import pickle
import numpy as np
from movielens import *

#load all the data required 
top_n=0
cluster_num=0
mapping=[]
item=[]
with open("meta_info", "r") as f:
    top_n=int( f.readline().rstrip("\n"))
    cluster_num=int( f.readline().rstrip("\n"))
    mapping=list( map(int, f.read().splitlines() ))

mat=pickle.load(open("utility_matrix.pkl", "rb") ) 
d = Dataset()
d.load_items("data/u.item", item)
#       self.id = int(id)                           
#       self.title = title
#       self.release_date = release_date
#       self.video_release_date = video_release_date
#       self.imdb_url = imdb_url
def get_cluster(id):
    cluster_id=mapping[id]
    index=[i for i,e in enumerate(mapping) if e==cluster_id and i!=id][:10]
    for each in index:
        print("Film id:\t{}|\tFilm Title:\t{}\n".format(item[each].id, item[each].title) )

user_id=int( input("UserID:") )
id=int(input("The Film that you like:"))
print("You like {}: {}\n".format(id, item[id].title))
print("Your avg score for this class is {}\n".format(mat[user_id, mapping[id] ]))
print("You might also like:\n")
get_cluster(id)
