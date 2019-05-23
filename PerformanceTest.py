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
    business = fields.Nested(Business,many=True)

#####Data Functions

def rec():
    uid='5caad264ebe5d49edbaa526c'
    #recom=get_db().user.find_one({'_id': ObjectId(var_u)}, {'birthyear': 1, 'firstname': 1})
        # set profile variables for GraphQL
    recom = [c_user.find_one({'_id': ObjectId(uid)}, {'birthyear': 1, 'firstname': 1}),
            c_profile.find_one({'userid': (uid)}, {'_id': 0, 'price': 1, 'alcohol': 1, 'cuisine': 1
            , 'dietrestrictions': 1, 'gender': 1, 'homezipcode': 1, 'workzipcode': 1})]

    price_in = '"' + (str(len(recom[1]['price']))) + '"'
    location_in = '"' + recom[1]['homezipcode'] + '"'
    cat_in = '"' + recom[1]['cuisine'].lower() + ',' + recom[1]['dietrestrictions'].lower() + '"'

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
            id
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
    merged[1]['_id']=uid     #this needs to be converted back to value
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
    return merged

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
    merged = [after_res]
    amerged = {'business': merged[0]['data']['search']['business']
               }
    return amerged


@app.route('/')
def hello():
    count = 1
    return 'Hello World! I have been seen {} times.\n'.format(count)



def isn():
        uid = request.args['uid']
        Business().booked='Yes' #revisit
        schema = recommend()
        schema.jit = toastedmarshmallow.Jit
        merged = (rec(uid))

        c_recom.insert_one(merged)


merged = (rec())
c_recom.insert_one(merged)

