# ***********************************************************************************
# File Name: twilio.py
# Author: Dimitar
# Created: 2020-03-12
# Description: Twilio Module For Global Usage
# -----------------------------------------------------------------------------------

import time
from twilio.rest import Client
from threading import Lock

lock = Lock()

# ***********************************************************************************
# @Function: Send Sms
# @Returns: Status Code
# -----------------------------------------------------------------------------------
def sendSms(account_sid, auth_token, src_phonenumber, dest_phonenumber, sms_body):
    try:
        lock.acquire()
        time.sleep(2)
        client = Client(account_sid, auth_token)
        message = client.messages.create(body=sms_body, from_=src_phonenumber, to=dest_phonenumber)
        lock.release()
        return True

    except Exception as e:
        return False