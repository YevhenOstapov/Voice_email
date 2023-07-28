# ***********************************************************************************
# File Name: basic.py
# Author: Dimitar
# Created: 2020-02-21
# Description: Basic Information Module For AutoserviceDashboard
# -----------------------------------------------------------------------------------

import json
import datetime
from datetime import timedelta

from autoservices.database.models import *

# ***********************************************************************************
# @Function: Check If All Keys in Key Array Is In Dict
# @Return: Status Code
# -----------------------------------------------------------------------------------
def checkKeysInDict(key_ary, dict_obj):
    for key in key_ary:
        if key not in dict_obj:
            return False
    return True


# ***********************************************************************************
# @Function: Get Date Period By Id
# @Return: From Date, To Date
# -----------------------------------------------------------------------------------
def getDatePeriodById(period_id):
    try:
        today = datetime.datetime.today()
        if period_id == 1:
            from_date = today
            to_date = from_date

        elif period_id == 2:
            from_date = today + timedelta(days=-1)
            to_date = from_date

        elif period_id == 3:
            last_monday = today + timedelta(days=-today.weekday())
            from_date = last_monday + timedelta(days=-7)
            to_date = from_date + timedelta(days=6)

        elif period_id == 4:
            f_day = today.replace(day=1)
            to_date = f_day + timedelta(days=-1)
            from_date = to_date.replace(day=1)

        elif period_id == 5:
            pass

        elif period_id == 6:
            from_date = today + timedelta(days=-today.weekday())
            to_date = from_date + timedelta(days=6)

        elif period_id == 10:
            from_date = today + timedelta(days=-today.weekday())
            to_date = from_date + timedelta(days=6)

        else:
            return None, None

        return from_date, to_date

    except Exception as e:
        return None, None




# ***********************************************************************************
# @Function: Get Date String
# @Return: DateStr
# -----------------------------------------------------------------------------------
def date2Str(date_obj):
    year = str(date_obj.year)
    month = date_obj.month
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)
    day = date_obj.day
    if day < 10:
        day = "0" + str(day)
    else:
        day = str(day)
    return year + "-" + month + "-" + day


# ***********************************************************************************
# @Function: Splite Time
# @Return: Hour, Minute
# -----------------------------------------------------------------------------------
def spliteTime(s_time):
    try:
        part0 = s_time.split(" ")[0]
        part1 = s_time.split(" ")[1]

        hour = part0.split(":")[0].lstrip("0")
        minute = part0.split(":")[1].lstrip("0")
        if hour == "":
            hour = 0
        else:
            hour = int(hour)
        if minute == "":
            minute = 0
        else:
            minute = int(minute)

        if part1.find("AM") != -1 and hour == 12:
            hour = 0
        if part1.find("PM") != -1 and hour != 12:
            hour += 12
        return hour, minute

    except Exception as e:
        return None, None

# ***********************************************************************************
# @Function: Get Next WeekDay
# @Return: DateObject
# -----------------------------------------------------------------------------------
def nextWeekday(d, weekday):
    days_ahead = weekday - d.weekday()
    return d + datetime.timedelta(days_ahead)


# ***********************************************************************************
# @Function: Get Company List
# @Return: Company List
# -----------------------------------------------------------------------------------
def getCompanyList(filter_str=""):
    try:
        company_list = []
        company_obj_list = list(tbl_company.objects.all())
        for company_obj in company_obj_list:
            flg = False
            if company_obj.name.find(filter_str) != -1:
                flg = True

            if flg == False:
                continue
            company_list.append({
                "id": company_obj.id,
                "name": company_obj.name,
                "group": company_obj.group,
                "twilio_account_sid": company_obj.twilio_account_sid,
                "twilio_auth_token": company_obj.twilio_auth_token,
                "twilio_phone_number": company_obj.twilio_phone_number,
                "customerInfoAPI": company_obj.customerInfoAPI,
                "fallbackForwardTo": company_obj.fallbackForwardTo,
                "unregisteredForwardTo": company_obj.unregisteredForwardTo,
                "unregisteredEmailTo": company_obj.unregisteredEmailTo,
                "unregisteredSmsTo": company_obj.unregisteredSmsTo,
                "unregisteredAPICall": company_obj.unregisteredAPICall,
            })
        return company_list

    except Exception as e:
        return []

# ***********************************************************************************
# @Function: Get Company By Id
# @Returns: Company
# -----------------------------------------------------------------------------------
def getCompanyById(company_id):
    try:
        company_list = getCompanyList()
        for company in company_list:
            if company["id"] == company_id:
                return company
        return None
    except Exception as e:
        return None

# ***********************************************************************************
# @Function: Register Company
# @Return: Company Id
# -----------------------------------------------------------------------------------
def registerCompany(name, group, twilio_account_sid, twilio_auth_token, twilio_phone_number,customerInfoAPI,fallbackForwardTo,

                    unregisteredForwardTo, unregisteredEmailTo ,unregisteredSmsTo,unregisteredAPICall):
    try:
        company_obj = tbl_company()
        if len(list(tbl_company.objects.filter(name=name))) > 0:
            return -1
        company_obj.name = name
        company_obj.group = group
        company_obj.twilio_account_sid = twilio_account_sid
        company_obj.twilio_auth_token = twilio_auth_token
        company_obj.twilio_phone_number = twilio_phone_number
        company_obj.customerInfoAPI = customerInfoAPI
        company_obj.fallbackForwardTo = fallbackForwardTo
        company_obj.unregisteredForwardTo = unregisteredForwardTo
        company_obj.unregisteredEmailTo = unregisteredEmailTo
        company_obj.unregisteredSmsTo = unregisteredSmsTo
        company_obj.unregisteredAPICall = unregisteredAPICall
        company_obj.save()
        return company_obj.id

    except Exception as e:
        return None


# ***********************************************************************************
# @Function: Get Advisor List
# @Return: Advisor List
# -----------------------------------------------------------------------------------
def getAdvisorList(filter_str=""):
    try:
        advisor_list = []
        advisor_obj_list = list(tbl_advisor.objects.all())
        for advisor_obj in advisor_obj_list:
            flg = False
            if advisor_obj.name.find(filter_str) != -1:
                flg = True

            if flg == False:
                continue
            advisor_list.append({
                "id": advisor_obj.id,
                "name": advisor_obj.name,
                "phone_number": advisor_obj.phone_number,
                "company_id": advisor_obj.company_id,
                "email": advisor_obj.email,
                "buddy_list": json.loads(advisor_obj.buddy_list),
                "caller_response_template": advisor_obj.caller_response_template.replace("\n", "slashn").replace("\\", "slashopposite"),
                "advisor_response_template": advisor_obj.advisor_response_template.replace("\n", "slashn").replace("\\", "slashopposite"),
                "caller_text_response_template": advisor_obj.caller_text_response_template.replace("\n", "slashn").replace("\\", "slashopposite"),
                "manager_response_template": advisor_obj.manager_response_template.replace("\n","slashn").replace("\\", "slashopposite"),
                "bookingURL": advisor_obj.bookingURL,
                "configEscalationOnOff": advisor_obj.configEscalationOnOff,
                "filterMeetingOnOff": advisor_obj.filterMeetingOnOff,
                "promptMeetingOptions": advisor_obj.promptMeetingOptions,
                "filterVMOnOff": advisor_obj.filterVMOnOff,
                "confAskPermissionToText": advisor_obj.confAskPermissionToText,
                "configTimeoutVM": advisor_obj.configTimeoutVM,
                "configTimeoutNoVMLeft": advisor_obj.configTimeoutNoVMLeft,
                "promptGreeting": advisor_obj.promptGreeting,
                "promptMeetingConclusion": advisor_obj.promptMeetingConclusion,
                "promptVMOptions": advisor_obj.promptVMOptions,
                "promptVMStart": advisor_obj.promptVMStart,
                "promptVMPermission": advisor_obj.promptVMPermission,
                "promptVMConclusion": advisor_obj.promptVMConclusion,
                "promptFirstName": advisor_obj.promptFirstName,
                "callerMeetingTemplate": advisor_obj.callerMeetingTemplate,
                "advisorMeetingTemplate": advisor_obj.advisorMeetingTemplate,
                "includeRecording": advisor_obj.includeRecording,


            })
        return advisor_list

    except Exception as e:
        return []


# ***********************************************************************************
# @Function: Get Advisor By Phone Number
# @Return: Advisor
# -----------------------------------------------------------------------------------
def getAdvisorByPhoneNumber(phone_number):
    try:
        advisor_list = getAdvisorList()
        for advisor in advisor_list:
            if advisor["phone_number"] == phone_number:
                return advisor
        return None

    except Exception as e:
        return None


# ***********************************************************************************
# @Function: Get Replier Name By Id
# @Return: Replier Name
# -----------------------------------------------------------------------------------
def getReplierNameById(vm_id, replier_id):
    try:
        vm_obj = tbl_voicemail.objects.get(id=vm_id)
        advisor = getAdvisorByPhoneNumber(vm_obj.advisor_phone)
        buddy_list = advisor["buddy_list"]

        # ---------- wrong replier_id case --------- #
        if replier_id != 100 and replier_id > len(buddy_list):
            return None

        if replier_id == 100:
            replier_name = "Manager"
        elif replier_id == 0:
            replier_name = advisor["name"]
        else:
            replier_name = buddy_list[replier_id-1]["name"]

        return replier_name

    except Exception as e:
        return None


# ***********************************************************************************
# @Function: Register Advisor
# @Return: Advisor Id
# -----------------------------------------------------------------------------------
def registerAdvisor(advisor_info):
    try:
        advisor_obj = tbl_advisor()
        if len(list(tbl_advisor.objects.filter(name=advisor_info["name"]))) > 0:
            return -1
        advisor_obj.name = advisor_info["name"]
        advisor_obj.phone_number = advisor_info["phone_number"]
        advisor_obj.email = advisor_info["email"]
        advisor_obj.company_id = advisor_info["company_id"]
        advisor_obj.buddy_list = json.dumps(advisor_info["buddy_list"])
        advisor_obj.caller_response_template = advisor_info["caller_response_template"]
        advisor_obj.advisor_response_template = advisor_info["advisor_response_template"]
        advisor_obj.caller_text_response_template = advisor_info["caller_text_response_template"]
        advisor_obj.manager_response_template = advisor_info["manager_response_template"]
        advisor_obj.bookingURL = advisor_info["bookingURL"]

        if advisor_info["configEscalationOnOff"] == "off":
            advisor_info["configEscalationOnOff"] = 0
        else:
            advisor_info["configEscalationOnOff"] = 1
        advisor_obj.configEscalationOnOff = advisor_info["configEscalationOnOff"]

        if advisor_info["filterMeetingOnOff"] == "off":
            advisor_info["filterMeetingOnOff"] = 0
        else:
            advisor_info["filterMeetingOnOff"] = 1

        advisor_obj.filterMeetingOnOff = advisor_info["filterMeetingOnOff"]
        advisor_obj.promptMeetingOptions = advisor_info["promptMeetingOptions"]
        if advisor_info["filterVMOnOff"] == "off":
            advisor_info["filterVMOnOff"] = 0
        else:
            advisor_info["filterVMOnOff"] = 1
        advisor_obj.filterVMOnOff = advisor_info["filterVMOnOff"]
        if advisor_info["confAskPermissionToText"] == "off":
            advisor_info["confAskPermissionToText"] = 0
        else:
            advisor_info["confAskPermissionToText"] = 1
        advisor_obj.confAskPermissionToText = advisor_info["confAskPermissionToText"]
        advisor_obj.configTimeoutVM = advisor_info["configTimeoutVM"]
        advisor_obj.configTimeoutNoVMLeft = advisor_info["configTimeoutNoVMLeft"]
        advisor_obj.promptGreeting = advisor_info["promptGreeting"]
        advisor_obj.promptMeetingConclusion = advisor_info["promptMeetingConclusion"]
        advisor_obj.promptVMOptions = advisor_info["promptVMOptions"]
        advisor_obj.promptVMStart = advisor_info["promptVMStart"]
        advisor_obj.promptVMPermission = advisor_info["promptVMPermission"]
        advisor_obj.promptVMConclusion = advisor_info["promptVMConclusion"]
        advisor_obj.promptFirstName = advisor_info["promptFirstName"]
        advisor_obj.callerMeetingTemplate = advisor_info["callerMeetingTemplate"]
        advisor_obj.advisorMeetingTemplate = advisor_info["advisorMeetingTemplate"]
        if advisor_info["includeRecording"] == "off":
            advisor_info["includeRecording"] = 0
        else:
            advisor_info["includeRecording"] = 1
        advisor_obj.includeRecording = advisor_info["includeRecording"]

        advisor_obj.save()

        return advisor_obj.id

    except Exception as e:
        return None


# ***********************************************************************************
# @Function: Update Advisor
# @Return: Status Code
# -----------------------------------------------------------------------------------
def updateAdvisor(name, advisor_info):
    try:
        advisor_obj = tbl_advisor.objects.get(name=name)
        advisor_obj.phone_number = advisor_info["phone_number"]
        advisor_obj.email = advisor_info["email"]
        advisor_obj.company_id = advisor_info["company_id"]
        advisor_obj.buddy_list = json.dumps(advisor_info["buddy_list"])
        advisor_obj.caller_response_template = advisor_info["caller_response_template"]
        advisor_obj.advisor_response_template = advisor_info["advisor_response_template"]
        advisor_obj.caller_text_response_template = advisor_info["caller_text_response_template"]
        advisor_obj.manager_response_template = advisor_info["manager_response_template"]
        advisor_obj.bookingURL = advisor_info["bookingURL"]
        if advisor_info["configEscalationOnOff"] == "off":
            advisor_info["configEscalationOnOff"] = 0
        else:
            advisor_info["configEscalationOnOff"] = 1

        advisor_obj.configEscalationOnOff = advisor_info["configEscalationOnOff"]
        advisor_obj.promptMeetingOptions = advisor_info["promptMeetingOptions"]
        if advisor_info["filterMeetingOnOff"] == "off":
            advisor_info["filterMeetingOnOff"] = 0
        else:
            advisor_info["filterMeetingOnOff"] = 1

        advisor_obj.filterMeetingOnOff = advisor_info["filterMeetingOnOff"]
        advisor_obj.promptMeetingOptions = advisor_info["promptMeetingOptions"]
        if advisor_info["filterVMOnOff"] == "off":
            advisor_info["filterVMOnOff"] = 0
        else:
            advisor_info["filterVMOnOff"] = 1
        advisor_obj.filterVMOnOff = advisor_info["filterVMOnOff"]
        if advisor_info["confAskPermissionToText"] == "off":
            advisor_info["confAskPermissionToText"] = 0
        else:
            advisor_info["confAskPermissionToText"] = 1



        advisor_obj.confAskPermissionToText = advisor_info["confAskPermissionToText"]
        advisor_obj.configTimeoutVM = advisor_info["configTimeoutVM"]
        advisor_obj.configTimeoutNoVMLeft = advisor_info["configTimeoutNoVMLeft"]
        advisor_obj.promptGreeting = advisor_info["promptGreeting"]
        advisor_obj.promptMeetingConclusion = advisor_info["promptMeetingConclusion"]
        advisor_obj.promptVMOptions = advisor_info["promptVMOptions"]
        advisor_obj.promptVMStart = advisor_info["promptVMStart"]
        advisor_obj.promptVMPermission = advisor_info["promptVMPermission"]
        advisor_obj.promptVMConclusion = advisor_info["promptVMConclusion"]
        advisor_obj.promptFirstName = advisor_info["promptFirstName"]
        advisor_obj.callerMeetingTemplate = advisor_info["callerMeetingTemplate"]
        advisor_obj.advisorMeetingTemplate = advisor_info["advisorMeetingTemplate"]
        if advisor_info["includeRecording"] == "off":
            advisor_info["includeRecording"] = 0
        else:
            advisor_info["includeRecording"] = 1
        advisor_obj.includeRecording = advisor_info["includeRecording"]

        advisor_obj.save()

        return True

    except Exception as e:
        return False
