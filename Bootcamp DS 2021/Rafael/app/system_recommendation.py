import pandas as pd
import math
import operator

def distance(q, p):
    total = 0
    for i in range(0, len(q)):
        total += (q[i]-p[i])**2
    return math.sqrt(total)/len(q)


def neighbors(df, k_neighbors, user):
    distances = []
    user_games = df[df['User_ID'] == user]
    df_subset = df[df['User_ID'] != user]
    user_temp = []
    temp = []
    temp_id = 0

    for index, row in df_subset.iterrows():
        if row['Game'] in set(user_games['Game']):
            if row['User_ID'] == temp_id:
                temp.append(row['Rating'])
                user_temp.append(user_games.loc[user_games['Game'] == row['Game'], 'Rating'].iloc[0])
            elif temp_id == 0:
                temp_id = row['User_ID']
                temp.append(row['Rating'])
                user_temp.append(user_games.loc[user_games['Game'] == row['Game'], 'Rating'].iloc[0])
            else:
                dist = distance(user_temp, temp)
                distances.append((temp_id, dist))
                temp_id = row['User_ID']
                temp = []
                temp.append(row['Rating'])
                user_temp = []
                user_temp.append(user_games.loc[user_games['Game'] == row['Game'], 'Rating'].iloc[0])
    distances.sort(key=operator.itemgetter(1))
    neighbor_list =[]
    for i in range(k_neighbors):
        neighbor_list.append(distances[i])
    return neighbor_list
        
def recommend(user, neighbor_list, df):
    user_games = df[df['User_ID'] == user]
    dissim_games = []
    for neighbor in neighbor_list:
        temp = df[(df['User_ID'] == neighbor[0]) & (~df['Game'].isin(user_games['Game']))]
        for index, game in temp.iterrows():
            dissim_games.append((game['Game'], game['Rating']))
    dissim_games.sort(key=operator.itemgetter(0))
    flag = ""
    running_sum = 0
    rec_list = []
    count = 0
    for dis in dissim_games:
        if flag != dis[0]:
            if flag != "":
                rec_list.append((flag, running_sum/count))
            flag = dis[0]
            running_sum = dis[1]
            count = 1
        else:
            running_sum += dis[1]
            count += 1
    sort_list = sorted(rec_list, key=operator.itemgetter(1), reverse = True)
    return(sort_list)
        
def rec_games(rec_tuple):
    games = []
    for pair in rec_tuple:
        games.append(pair[0])
    return games

def knn(user, k_neighbors):
    df = pd.read_pickle("../data.pkl")
    knearest = neighbors(df, k_neighbors, user)
    rec_list = recommend(user, knearest, df)
    games = rec_games(rec_list)
    return games