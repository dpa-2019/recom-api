import os

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson import ObjectId
import requests
from datetime import datetime
import tzlocal  # $ pip install tzlocal

import toastedmarshmallow
from marshmallow import Schema, fields

# get current timezone for dates.
local_timezone = tzlocal.get_localzone()

#recom_dt = datetime.now(local_timezone).strftime("%d/%m/%Y %H:%M:%S")  # the current time
recom_dt = datetime.now(local_timezone)

#var_u = '5caad264ebe5d49edbaa526c'
# create an instance of Flask

app = Flask(__name__)
api = Api(app)

#Get Mongo DB
def get_db():
    client = MongoClient('mongodb+srv://dpa_admin:Buong123%21@cluster0-brbjx.mongodb.net/test?retryWrites=true')
    db=client.mydb
    return db


c_recom=get_db().recom
c_user=get_db().user
c_profile=get_db().profile

#Get Event Data

#####YELP GraphQL Call
headers = {
    "Authorization": "bearer Ey1kbIspQjmM0OAW1_6jX_EpxyLtdIE47eeFxUjj0nhtVc6Qtft7JocAo9GQVeazWIomrFwftlgc-prxkq8Ldx0N_5J9fV5wzIK1hAjwmoTxZpHR9ldkziiMineUXHYx"}

def run_query(query):  # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.yelp.com/v3/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

#####Foursquare


#####Data Objects

class Coord(Schema):
    latitude = fields.Str()
    longitude = fields.Str()

class Business(Schema):
    booked = fields.Str()
    id = fields.Str()
    name = fields.Str()
    alias = fields.Str()
    coordinates = fields.Nested(Coord)
    rating = fields.Str()
    phone  = fields.Str()
    photos = fields.Str()
    url =fields.Str()

class recommend(Schema):
    recom_dt = fields.DateTime()
    user_id =  fields.Str()
    firstname =fields.Str()
    birthyear = fields.Int()
    price =fields.Str()
    cuisine = fields.Str()
    diet = fields.Str()
    homezip = fields.Str()
    total = fields.Int()
    business = fields.Nested(Business, many=True)

#####Data Functions


def aftersrec(lat,lon):
    ####secondary recommendation - get long / lat of picked index array ("1" below)
    #### search for bars or desert by walking distance
    # var_type= restaurants,bars, desert etc..
    #lat = '34.054957345816'
    #lon = '-118.249773225864'
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
        id
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

    after_res = run_query(query_2)  # secondary recommendation
    merged=[after_res]
    amerged={'business': merged[0]['data']['search']['business']
            }
    return amerged

def afters():

        schema = Business()
        schema.jit = toastedmarshmallow.Jit
        afmerged = (aftersrec(lat='34.054957345816',lon='-118.249773225864'))

        return  afmerged  #schema.dump(afmerged, many=True)

print(afters())
