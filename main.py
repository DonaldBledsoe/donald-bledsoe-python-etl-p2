import pgsql
import sql  # necessary imports
import requests

import json

from datetime import datetime


def get_movie_data(title):
    headers = {"Authorization": "9855f49b"}
    request_url = f"https://www.omdbapi.com/?t={title}&apikey=686eed26"
    return requests.get(request_url, headers=headers).json()


if __name__ == '__main__':

    # pgsql.query(sql.create_schema)  # creating the schema

    pgsql.query(sql.create_tables)

    f = open("datasets/json/movies.json")
    reader = json.load(f)

    titlelist = []              #list to place titles in

    for i in reader:                            #for loop to extract titles only
        if i['year'] >= 2018:
            titlelist.append(i["title"])
    f.close()                                   #closing file

    seat = set(titlelist)                       #converting list to set
    #print(seat)

    newlist = list(seat)                        #putting my non-dupes into a new list

    """lastdata = {}               #dictionary f last set of data pulled from API
    for movie in newlist:                       #looping thru and getting data from API
        lastdata[movie] = get_movie_data(movie)

    f_write = open("datasets/json/filtered.json", 'w')      #writing data of filtered to a list
    json.dump(lastdata, f_write, indent=4)

    f_write.close()                             #closing
    
    print(lastdata)
    """

    value = "English"                           # setting the search criterion to English

    only_English = []                           # creating a list to hold the English movies
    f2 = open("datasets/json/filtered.json")    # opening the filtered json file
    reader2 = json.load(f2)                     #
    for k, v in reader2.items():                # outer for loop to start iterating dict of dicts
        for k1, v1 in v.items():
            if k1 == "Language":                # Language key is designated
                if value in v1:                 # value of English is selected for
                    only_English.append(v)      # appending it to only_English list

    # print(only_English, len(only_English))

    req_fields = []                             # creating a new list for the necessary final fields

    # specifying the table fields needed
    needed_keys = ["Title", "Rated", "Released", "Runtime", "Genre", "Director", "Writer", "Actors", "Plot", "Awards",
                   "Poster"]

    for i in only_English:
        sub_select = {key: i[key] for key in needed_keys}
        req_fields.append(sub_select)

    #print(req_fields, len(req_fields))


    # now filter for any movies that have an N/A in a value
    without_NA = []                             #new list for movies without an N/A entry

    for i in req_fields:                        #iterating thru and appending all movies that do NOT have an N/A entry
        if "N/A" not in i.values():
            without_NA.append(i)

    #print(without_NA, len(without_NA))

    # making a final list of movies that looks for year 2018 in the data that was retrieved from the API
    api_2018 = []                               # new list to hold final filtered data

    for i in without_NA:                        #for loop to do second filter
        if datetime.strptime(i['Released'], "%d %b %Y").year >= 2018:
            api_2018.append(i)                  # appending


    for movie in api_2018:
        last_final = []
        movie["Genre"] = movie["Genre"].split(',')              # splitting the lists of values
        movie["Writer"] = movie["Writer"].split(',')
        movie["Actors"] = movie["Actors"].split(',')
        movie["Runtime"] = int(movie["Runtime"][:3])
        last_final.append(movie["Title"])                       # appending the values for each of the required headers
        last_final.append(movie["Rated"])
        last_final.append(movie["Released"])
        last_final.append(movie["Runtime"])
        last_final.append(movie["Genre"])
        last_final.append(movie["Director"])
        last_final.append(movie["Writer"])
        last_final.append(movie["Actors"])
        last_final.append(movie["Plot"])
        last_final.append(movie["Awards"])
        last_final.append(movie["Poster"])

        pgsql.query(sql.insert_movie, last_final)               # inserting each movie into the db
