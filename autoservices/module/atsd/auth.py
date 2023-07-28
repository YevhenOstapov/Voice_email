# ***********************************************************************************
# File Name: basic.py
# Author: Dimitar
# Created: 2020-02-21
# Description: Authentication Module For AutoserviceDashboard
# -----------------------------------------------------------------------------------
import random

from django.contrib.auth import authenticate

from autoservices.database.models import *
from autoservices.module.atsd.constant.ret_code import *

# ***********************************************************************************
# @Function: Authenticate User
# @Returns: Ret Code, User Object
# -----------------------------------------------------------------------------------
def authenticateUser(user_email, user_pwd):
    try:
        user_obj = list(tbl_user.objects.filter(email=user_email))
        if len(user_obj) == 0:
            return AUTH_USER_NOT_FOUND, None
        user_obj = user_obj[0]

        if user_obj.is_active == 0:
            return AUTH_ACCOUNT_DISABLED, None

        user = authenticate(username=user_email, password=user_pwd)
        if user == None:
            return AUTH_WRONG_PWD, None

        return AUTH_SUCCESS, user

    except Exception as e:
        return AUTH_UNKOWN_ERROR, None


# ***********************************************************************************
# @Function: Register User
# @Returns: Ret Code, User Object
# -----------------------------------------------------------------------------------
def registerUser(email, first_name, last_name, phone_number, company_id, factor_booked, factor_transfer, agents, advisors, reports):
    try:
        if len(list(tbl_user.objects.filter(email=email))) > 0:
            return REG_EXISTING_EMAIL, None

        uid = random.randint(10000000, 99999999)
        while len(list(tbl_user.objects.filter(uid=uid))) > 0:
            uid = random.randint(10000000, 99999999)

        user_obj = tbl_user()
        user_obj.uid = uid
        user_obj.email = email
        user_obj.username = email
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.phone_number = phone_number
        user_obj.company_id = company_id
        user_obj.factor_booked = factor_booked
        user_obj.factor_transfer = factor_transfer
        user_obj.agents = agents
        user_obj.advisors = advisors
        user_obj.reports = reports

        user_obj.set_password("vg%9P?HVs96`8Qnvj792<HJ)dw!V7c923kxky'I!/[")
        user_obj.save()

        return REG_SUCCESS, user_obj

    except Exception as e:
        return REG_UNKOWN_ERROR, None