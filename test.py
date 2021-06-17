import pymongo
from datetime import datetime

# client = pymongo.MongoClient("mongodb+srv://bths:BThSProject1.0@testcluster.f7oii.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
# client = pymongo.MongoClient("mongodb://localhost:27017/timepass")



# client.db.users.insert_one({'username':'bths','password':'BThSProject1.0','activity':[{'Login':datetime.now()}]})
# client.db.users.update_one({'username':'bths'},{'$push': {'activity': {'Logout': datetime.now()}}})

import requests
import random
import json

rand=random.randint(1,999999)

msg=f"Your One Time Password(OTP) is {rand} and verify it on whatsapp hope you know my number katti terese ja"

def sms_send(a,msg):
    url="https://www.fast2sms.com/dev/bulk"
    params={
#    // Paste Your Unique API Here in-place of ************
        "authorization":"gDmCEZnP1KstGl0LH5JyXFVvdwx7Tqp3f2kA4ejRY9U6hMSozWhrSgw3DjQ89oXKONGPlBLiafYHuq6A",
        "sender_id":"BYEINC.",
        "message":msg,
        "language":"english",
        "route":"p",
        "numbers":a
    }
    rs=requests.get(url,params=params)


def send():
    number = 9653627810
    sms_send(number,msg)

send()


from user_models import models

