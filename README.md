# recom-api


##install docker, install compose


##Usage

'''json
{
    "data": "event triggers, user profile and recommended businesses",
    "message": "recommend business, booked business, recommend after event, pull event history"

}
'''

## Definintions


Trigger: User intake triggers recommendation event. Uses: User_Id and intake preference.

'GET and POST /recommendations'

**Response**

-'200 OK' on success

'''json
[
    {
        "user_id": "user.user_id"
        "business_id": "business id"
        "name" : "business name "
        "alias" : "business alias"
         coordinates{latitude,longitude}
        "rating": "rating""
        "phone" : "business  phone""
        "photos": "Photo URL"
        "url" : "business url (depends on service)"
    }
    
]
'''

## Gets close by recommendations based on longitiude and latitude of business
## booked

Trigger: User books event , Use: business longitiude and latitude, and profile preference/history.


'GET /after'

**Response**

-'200 OK' on success

'''json
[
    {
        "user_id": "user.user_id"
        "business_id": "business id"
        "name" : "business name "
        "alias" : "business alias"
         coordinates{latitude,longitude}
        "rating": "rating""
        "phone" : "business  phone""
        "photos": "Photo URL"
        "url" : "business url (depends on service)"
    }
    
]
'''

## Gets booked event history
## booked

Trigger: ??


'GET /history'

**Response**

-'200 OK' on success

'''json
[
    {
        "user_id": "user.user_id"
        "business_id": "business id"
        "name" : "business name "
        "bdate" : "booked date"
        "rating": "rating""
        "phone" : "business  phone""
        "photos": "Photo URL"
        "url" : "business url (depends on service)"
    }
    
]
'''