"""
#Installs
pip install django
pip install graphene_django\python -m pip install pymongo
python -m pip install pymongo
pip install dnspython
pip install StringIO
pip install tzlocal

Charles B 4/11/2019 Create initial
            Pull data from app and query Yelp API and to create recommended.


"""
import pymongo
from pymongo import MongoClient
from bson import ObjectId
import pprint
import requests
from pytz import timezone
from datetime import datetime
import tzlocal  # $ pip install tzlocal
import json

# get current timezone for dates.
local_timezone = tzlocal.get_localzone()
recom_dt = datetime.now(local_timezone).strftime("%d/%m/%Y %H:%M:%S")  # the current time

# pass in user id
# var_u='5ca81f69ebe5d49edb7dac51'
var_u = '5caad264ebe5d49edbaa526c'

# var_type pass in "restaurants, bars or desert" for secondary recommendation.


# Connect to Mongo and set db & documents

client = MongoClient('mongodb+srv://dpa_admin:Buong123%21@cluster0-brbjx.mongodb.net/test?retryWrites=true')
db = client.mydb
c_user = db.user
c_profile = db.profile
c_recom = db.recom


#set profile variables for GraphQL
recom = [c_user.find_one({'_id': ObjectId(var_u)}, {'birthyear': 1, 'firstname': 1}),
         c_profile.find_one({'userid': (var_u)}, {'_id': 0, 'price': 1, 'alcohol': 1, 'cuisine': 1
             , 'dietrestrictions': 1, 'gender': 1, 'homezipcode': 1, 'workzipcode': 1})]

price_in = '"' + (str(len(recom[1]['price']))) + '"'
location_in = '"' + recom[1]['homezipcode'] + '"'
cat_in = '"' + recom[1]['cuisine'].lower() + ',' + recom[1]['dietrestrictions'].lower() + '"'

#GraphQL Call
headers = {
    "Authorization": "bearer Ey1kbIspQjmM0OAW1_6jX_EpxyLtdIE47eeFxUjj0nhtVc6Qtft7JocAo9GQVeazWIomrFwftlgc-prxkq8Ldx0N_5J9fV5wzIK1hAjwmoTxZpHR9ldkziiMineUXHYx"}


def run_query(query):  # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.yelp.com/v3/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


query = """{
    search (term: "restaurants",
    categories:""" + cat_in + """,
    location:""" + location_in + """,
    price: """ + price_in + """,
    limit: 30,
    radius:20000
    sort_by: "rating") {
    total
    business
{
    name
    alias
    coordinates{latitude
                longitude}
    rating
    phone
    photos
    url
}
}
} """

result = run_query(query)  # execute query

merged = [recom_dt, recom[0], recom[1], result]

# merged = {'recom_dt':recom_dt, [recom[:]]}

merged = {'recom_dt': merged[0],
          "user_id": merged[1]['_id'],
          "firstname": merged[1]['firstname'],
          "birthyear": merged[1]['birthyear'],
          "price": merged[2]['price'],
          "cuisine": merged[2]['cuisine'],
          "diet": merged[2]['dietrestrictions'],
          "homezip": merged[2]['homezipcode'],
          "total": merged[3]['data']['search']['total'],
          "business": merged[3]['data']['search']['business']
          }

# Insert into DB Mongo and Pass JSON

# r = c_recom.insert_one(merged)


####use coordinates from merged array to create secondary recomendation.

####secondary recommendation - get long / lat of picked index array ("1" below)
#### search for bars or desert by walking distance

lat = str((merged['business'][1]['coordinates']['latitude']))
lon = str((merged['business'][1]['coordinates']['longitude']))

query_2 = """{
    search (term: "bar", 
    latitude:""" + lat + """,
    longitude:""" + lon + """,
    limit: 30,
    radius:500
    sort_by: "rating") {
    total
    business
{
    name
    alias
    coordinates {latitude
                longitude}
    rating
    phone
    photos
    url
}
}
} """

result_2 = run_query(query_2)  # secondary recommendation

print(result_2)

#build secondary recommendation load mongo.
