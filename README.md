# recom-api


##install docker, install compose
https://docs.docker.com/install/linux/docker-ce/debian/
https://docs.docker.com/compose/install/

Linux Docker Install:
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https:d//download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic test"
sudo apt update
sudo apt install docker-ce

Remove Images:
$ docker images
$ t 

$ docker ps -a
$ docker rm $(docker ps -qa --no-trunc --filter "status=exited")


To Run with Only Docker:
$ docker build -t dpa .
$ docker run -p 80:5000 dpa

##Usage
## 4 API Calls

'''json
{
    "data": "event triggers, user profile and recommended businesses",
    "message": "recommend business, booked business, recommend after event, pull event history"

}
'''

## Definintions


Trigger: User intake triggers recommendation event. Uses: User_Id and intake preference. User and
preferences are unique row , businesses are nested arrays.

#URL
http://0.0.0.0:5000/recom?uid=5caad264ebe5d49edbaa526c

#API 1
'GET' method will use API Keys to pull event data.
#API 2
'POST' method will post data of same structure to mongo database.

**Response**

-'200 OK' on success

'''json
{
        "birthyear": 1993,
        "business": [
            {
                "alias": "patina-restaurant-los-angeles-2",
                "coordinates": {
                    "latitude": "34.054957345816",
                    "longitude": "-118.249773225864"
                },
                "id": "c1g6WMRsJ9yrv0D_fyhlpw",
                "name": "Patina Restaurant",
                "phone": "+12139723331",
                "photos": "['https://s3-media4.fl.yelpcdn.com/bphoto/-hLdyJgdI3ngiU8i7XQFkw/o.jpg']",
                "rating": "4.0",
                "url": "https://www.yelp.com/biz/patina-restaurant-los-angeles-2?adjust_creative=Wcg0rEKJ6YDQmjvxsGXVSQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_graphql&utm_source=Wcg0rEKJ6YDQmjvxsGXVSQ"
            },
            {
                "alias": "le-comptoir-los-angeles-3",
                "coordinates": {
                    "latitude": "34.0634014842636",
                    "longitude": "-118.300578072667"
                },
                "id": "JI5nDSILR7XPY5T7xTQ1VA",
                "name": "Le Comptoir",
                "phone": "+12132900750",
                "photos": "['https://s3-media3.fl.yelpcdn.com/bphoto/u1k9nxdqGkrEIcygi9Gw-A/o.jpg']",
                "rating": "4.0",
                "url": "https://www.yelp.com/biz/le-comptoir-los-angeles-3?adjust_creative=Wcg0rEKJ6YDQmjvxsGXVSQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_graphql&utm_source=Wcg0rEKJ6YDQmjvxsGXVSQ"
            }
        ],
        "cuisine": "French",
        "diet": "Kosher",
        "firstname": "Cynthia",
        "homezip": "91801",
        "price": "$$$$",
        "recom_dt": "2019-05-22T05:49:44.710246+00:00",
        "total": 2,
        "user_id": "5caad264ebe5d49edbaa526c"
    },
    {}
]

'''

## Gets close by recommendations based on longitiude and latitude of business
## booked

Trigger: User books event, the longitude and latitude of the booked event will be used 
to find walkable places - will also use profile preference/history.

#API 3
'GET /after'

#URL
http://0.0.0.0:5000/afters?lat=34.054957345816&lon=-118.249773225864

**Response**

#-'200 OK' on success need to fix - can't use Marshmallow...used Jsonify.

'''json
{
    "business": [
        {
            "alias": "grand-performances-los-angeles",
            "coordinates": {
                "latitude": 34.05166,
                "longitude": -118.25138
            },
            "id": "KM0vgUk-ULUSLgViw0TZxQ",
            "name": "Grand Performances",
            "phone": "+12136872190",
            "photos": [
                "https://s3-media2.fl.yelpcdn.com/bphoto/PLZ-_p1WUpuSjsdMlfZvXQ/o.jpg"
            ],
            "rating": 5,
            "url": "https://www.yelp.com/biz/grand-performances-los-angeles?adjust_creative=Wcg0rEKJ6YDQmjvxsGXVSQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_graphql&utm_source=Wcg0rEKJ6YDQmjvxsGXVSQ"
        },
    
    
]
'''

## Gets booked event history
## booked

Trigger: Uses User Id to get user history , should have "booked flag set to yes as a filter"
#URL
http://0.0.0.0:5000/hist?uid=5caad264ebe5d49edbaa526c

#API 4
'GET /history'



**Response**

-'200 OK' on success

'''json
{
    "business": [
        {
            "alias": "grand-performances-los-angeles",
            "coordinates": {
                "latitude": 34.05166,
                "longitude": -118.25138
            },
            "id": "KM0vgUk-ULUSLgViw0TZxQ",
            "name": "Grand Performances",
            "phone": "+12136872190",
            "photos": [
                "https://s3-media2.fl.yelpcdn.com/bphoto/PLZ-_p1WUpuSjsdMlfZvXQ/o.jpg"
            ],
            "rating": 5,
            "url": "https://www.yelp.com/biz/grand-performances-los-angeles?adjust_creative=Wcg0rEKJ6YDQmjvxsGXVSQ&utm_campaign=yelp_api_v3&utm_medium=api_v3_graphql&utm_source=Wcg0rEKJ6YDQmjvxsGXVSQ"
        }
'''