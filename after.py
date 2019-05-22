"""
#Installs
pip install django
pip install graphene_django\python -m pip install pymongo
python -m pip install pymongo
pip install dnspython
pip install StringIO
pip install tzlocal

Charles B 4/11/2019 Create initial
            Take selected location (lat and long) and recommend places after.


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

# var_type pass in "restaurants, bars or desert" for secondary recommendation.


# Connect to Mongo and set db & documents

client = MongoClient('mongodb+srv://dpa_admin:Buong12zSS3%21@cluster0-brbjx.mongodb.net/test?retryWrites=true')
db = client.mydb
c_user = db.user
c_profile = db.profile
c_recom = db.recom

print(c_recom['business']['coordinates'])

# GraphQL Call
headers = {
    "Authorization": "bearer Ey1kbIspQjmM0OAW1_6jX_EpxyLtdIE47eeFxUjj0nhtVc6Qtft7JocAo9GQVeazWIomrFwftlgc-prxkq8Ldx0N_5J9fV5wzIK1hAjwmoTxZpHR9ldkziiMineUXHYx"}


def run_query(query):  # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.yelp.com/v3/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


####use coordinates from merged array to create secondary recomendation.

####secondary recommendation - get long / lat of picked index array ("1" below)
#### search for bars or desert by walking distance
# var_type= restaurants,bars, desert etc..
lat = '34.054957345816'
lon = '-118.249773225864'

query_2 = """{
    search (term: "bar", 
    latitude:""" + lat + """,
    longitude:""" + lon + """,
    limit: 20,
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

# build secondary recommendation load mongo.
