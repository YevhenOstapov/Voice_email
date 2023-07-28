# ***********************************************************************************
# File Name: report.py
# Author: Dimitar
# Created: 2020-02-24
# Description: Report Module For autoservices
# -----------------------------------------------------------------------------------

import requests
import json
import math
import datetime
from datetime import timedelta

from autoservices.database.models import *
from autoservices.module.glb.constant.http_ret_code import *
from autoservices.module.atsd.constant.project import *
from autoservices.module.atsd import basic as atsd_basic
from autoservices.module.atsd import user as atsd_user

# ***********************************************************************************
# @Function: Get Count Of Event
# @Return: Count of Event
# -----------------------------------------------------------------------------------
def callEventCountApi(event_name, agent_code, from_date, to_date):
    try:
        # url = API_BASIC_URL + "getEventCount?"
        url = mongo_count_url+"?secret=123123"
        s_from_date = atsd_basic.date2Str(from_date)
        s_to_date = atsd_basic.date2Str(to_date)

        # url = "https://us-east-1.aws.webhooks.mongodb-realm.com/api/client/v2.0/app/application-0-qsljw/service/count-event-data/incoming_webhook/count-event-data?secret=123123&agent=testagent&eventName=testevent&date1=2021-11-16&date2=2021-11-18"
        # url = url + "agent=" + agent_code + "&eventName=" + event_name + "&dateFrom=" + s_from_date + "&dateTo=" + s_to_date
        url = url + "&agent=" + agent_code + "&eventName=" + event_name + "&dateFrom=" + s_from_date + "&dateTo=" + s_to_date
        print(url)
        res = requests.get(url)

        if res.status_code != HttpResponse200:
            return None
        # print("here")
        value=res.json()

        # print(value.get("$numberLong"))
        return value.get("$numberLong")
        # return res.json()[0]["count"]
    except Exception as e:
        return None


# ***********************************************************************************
# @Function: Get Event List
# @Return: Event List
# -----------------------------------------------------------------------------------
def callEventListApi(event_name, agent_code, from_date, to_date):
    try:
        # url = API_BASIC_URL + "getEventData?"
        url = mongo_getdata_url +"?secret=123123"

        s_from_date = atsd_basic.date2Str(from_date)
        s_to_date = atsd_basic.date2Str(to_date)
        # url = url + "agent=" + agent_code + "&eventName=" + event_name + "&dateFrom=" + s_from_date + "&dateTo=" + s_to_date
        url = url + "&agent=" + agent_code + "&eventName=" + event_name + "&dateFrom=" + s_from_date + "&dateTo=" + s_to_date

        res = requests.get(url)

        if res.status_code != HttpResponse200:
            return None
        return res.json()
    except Exception as e:
        return None


# --------------------------------- Report 1 --------------------------------- #

# ***********************************************************************************
# @Function: Get Booked Indicator Data
# @Return: Booked Indicator Data
# -----------------------------------------------------------------------------------
def getBookedIndicatorData(user_email, agent_id, from_date, to_date):
    try:
        user_obj = tbl_user.objects.get(email=user_email)
        agent_obj = tbl_agent.objects.get(id=agent_id)
        agent_code = agent_obj.code
        cnt_scheduling = callEventCountApi("scheduleStartAutoServ", agent_code, from_date, to_date)
        cnt_booked = callEventCountApi("scheduleCompleteAutoServ", agent_code, from_date, to_date)
        cnt_transferred = callEventCountApi("operator", agent_code, from_date, to_date)

        #
        print("cnt_scheduling=",cnt_scheduling)
        print("cnt_booked=",cnt_booked)
        print("cnt_transferred=",cnt_transferred)




        if cnt_scheduling == None or cnt_booked == None or cnt_transferred == None:
            return None
        # print("data is not here")
        # print( user_obj.factor_booked,"test user_obj")
        # print(type(user_obj.factor_booked))
        cnt_booked = math.ceil(int(cnt_booked) * user_obj.factor_booked)
        # print("cnt_booked_check",cnt_booked)
        cnt_transferred = math.ceil(int(cnt_transferred) * user_obj.factor_transfer)
        # print("cnt_transferred",cnt_transferred)
        # print("go")

        # ---------- get last week, current week booked calls ---------- #
        t_from_date, t_to_date = atsd_basic.getDatePeriodById(3)

        # print(t_from_date, t_to_date, "t_from_date")

        cnt_l_week_booked = callEventCountApi("scheduleCompleteAutoServ", agent_code, t_from_date, t_to_date)

        # print(cnt_l_week_booked, "cnt_l_week_booked")

        t_from_date, t_to_date = atsd_basic.getDatePeriodById(10)
        # print(t_from_date,"cnt_l_week_booked")

        cnt_c_week_booked = callEventCountApi("operator", agent_code, t_from_date, t_to_date)


        if cnt_l_week_booked == None or cnt_c_week_booked == None:
            return None
        # print("not none")
        cnt_l_week_booked = math.ceil(int(cnt_l_week_booked) * user_obj.factor_booked)
        cnt_c_week_booked = math.ceil(int(cnt_c_week_booked) * user_obj.factor_booked)

        data = {
            "cnt_scheduling": cnt_scheduling,
            "cnt_booked": cnt_booked,
            "cnt_transferred": cnt_transferred,
            "cnt_l_week_booked": cnt_l_week_booked,
            "cnt_c_week_booked": cnt_c_week_booked
        }
        print(data, "sucess")
        return data


    except Exception as e:
        return None


# ***********************************************************************************
# @Function: Get Inbound Indicator Data
# @Return: Inbound Indicator Data
# -----------------------------------------------------------------------------------
def getInboundIndicatorData(user_email, agent_id, from_date, to_date):
    try:
        agent_obj = tbl_agent.objects.get(id=agent_id)
        agent_code = agent_obj.code
        cnt_incoming = callEventCountApi("incomingCall", agent_code, from_date, to_date)
        cnt_non_scheduling = callEventCountApi("escalation", agent_code, from_date, to_date)
        # print("incomingcall",cnt_incoming)
        # print("escalation",cnt_non_scheduling)
        if cnt_incoming == None or cnt_non_scheduling == None:
            return None

        # ---------- get last week, current week incoming calls ---------- #
        t_from_date, t_to_date = atsd_basic.getDatePeriodById(3)
        cnt_l_week_incoming = callEventCountApi("incomingCall", agent_code, t_from_date, t_to_date)

        t_from_date, t_to_date = atsd_basic.getDatePeriodById(10)
        cnt_c_week_incoming = callEventCountApi("incomingCall", agent_code, t_from_date, t_to_date)

        if cnt_l_week_incoming == None or cnt_c_week_incoming == None:
            return None

        data = {
            "cnt_incoming": cnt_incoming,
            "cnt_non_scheduling": cnt_non_scheduling,
            "cnt_l_week_incoming": cnt_l_week_incoming,
            "cnt_c_week_incoming": cnt_c_week_incoming
        }

        return data

    except Exception as e:
        return None


# ***********************************************************************************
# @Function: Get Transfer Indicator Data
# @Return: Transfer Indicator Data
# -----------------------------------------------------------------------------------
def getTransferIndicatorData(user_email, agent_id, from_date, to_date):
    try:
        agent_obj = tbl_agent.objects.get(id=agent_id)
        agent_code = agent_obj.code

        cnt_operator = callEventCountApi("operator", agent_code, from_date, to_date)
        cnt_order = callEventCountApi("order", agent_code, from_date, to_date)
        print("transfer in getTransferIndicatorData ")
        if cnt_operator == None or cnt_order == None:
            return None

        cnt_operator_order = cnt_operator + cnt_order

        data = {
            "cnt_operator_order": cnt_operator_order,
            "cnt_order": cnt_order
        }

        return data

    except Exception as e:
        return None


# ***********************************************************************************
# @Function: Get Event Count Of Afterhour
# @Return: Count Of Afterhour
# -----------------------------------------------------------------------------------
def getCountOfAfterHour(event_list, s_openweekly_from, s_openweekly_to, s_opensat_from, s_opensat_to):
    cnt_after_hour = 0
    # print("getCountOfAfterHour1",event_list,s_openweekly_from,s_openweekly_to,s_opensat_from,s_opensat_to)
    openweekly_from_hour, openweekly_from_min = atsd_basic.spliteTime(s_openweekly_from)
    openweekly_to_hour, openweekly_to_min = atsd_basic.spliteTime(s_openweekly_to)
    opensat_from_hour, opensat_from_min = atsd_basic.spliteTime(s_opensat_from)
    opensat_to_hour, opensat_to_min = atsd_basic.spliteTime(s_opensat_to)
    # print("hour 3")
    # obj = datetime.datetime.strptime("2021-11-18T012:46:07.135Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    # obj = datetime.datetime.strptime("2021-11-18T01:46:07.135Z", "%Y-%m-%dT%H:%M:%S.%fZ")
    # print(obj)
    for event in event_list:
        date_val=event["Date"]

        # print(date_val)
        time_obj = datetime.datetime.strptime(date_val, "%Y-%m-%dT%H:%M:%S.%fZ")


        # print(time_obj.weekday())
        if time_obj.weekday() == 6:
            cnt_after_hour += 1
            continue

        if time_obj.weekday() < 5:
            from_hour = openweekly_from_hour
            from_min = openweekly_from_min
            to_hour = openweekly_to_hour
            to_min = openweekly_to_min
        else:
            from_hour = opensat_from_hour
            from_min = opensat_from_min
            to_hour = opensat_to_hour
            to_min = opensat_to_min

        if (from_hour > time_obj.hour) or (from_hour == time_obj.hour and from_min > time_obj.minute):
            cnt_after_hour += 1
            continue
        if (to_hour < time_obj.hour) or (from_hour == time_obj.hour and to_min < time_obj.minute):
            cnt_after_hour += 1
            continue

    return cnt_after_hour


# ***********************************************************************************
# @Function: Get Afterhour Indicator Data
# @Return: Afterhour Indicator Data
# -----------------------------------------------------------------------------------
def getAfterhourIndicatorData(user_email, agent_id, from_date, to_date):
    try:
        agent_obj = tbl_agent.objects.get(id=agent_id)
        agent_code = agent_obj.code

        incoming_list = callEventListApi("incomingCall", agent_code, from_date, to_date)
        # print("agent is not here")
        # print(incoming_list,"incoming_list is here")


        if incoming_list == None:
            # print("incominglist_is here")
            return None
        # print("step1")
        cnt_incoming_afterhour = getCountOfAfterHour(incoming_list,
                                                     agent_obj.open_weekly_from,
                                                     agent_obj.open_weekly_to,
                                                     agent_obj.open_sat_from,
                                                     agent_obj.open_sat_to)
        # print("here is bug")
        # print(cnt_incoming_afterhour)

        booked_list = callEventListApi("scheduleCompleteAutoServ", agent_code, from_date, to_date)
        cnt_booked_afterhour = getCountOfAfterHour(booked_list,
                                                   agent_obj.open_weekly_from,
                                                   agent_obj.open_weekly_to,
                                                   agent_obj.open_sat_from,
                                                   agent_obj.open_sat_to)

        scheduling_list = callEventListApi("scheduleStartAutoServ", agent_code, from_date, to_date)
        cnt_scheduling_afterhour = getCountOfAfterHour(scheduling_list,
                                                       agent_obj.open_weekly_from,
                                                       agent_obj.open_weekly_to,
                                                       agent_obj.open_sat_from,
                                                       agent_obj.open_sat_to)

        # ---------- get last week, current week incoming afterhour calls ---------- #
        t_from_date, t_to_date = atsd_basic.getDatePeriodById(3)
        l_week_incoming_list = callEventListApi("incomingCall", agent_code, t_from_date, t_to_date)
        cnt_l_week_incoming_afterhour = getCountOfAfterHour(l_week_incoming_list,
                                                            agent_obj.open_weekly_from,
                                                            agent_obj.open_weekly_to,
                                                            agent_obj.open_sat_from,
                                                            agent_obj.open_sat_to)

        t_from_date, t_to_date = atsd_basic.getDatePeriodById(10)
        c_week_incoming_list = callEventListApi("incomingCall", agent_code, t_from_date, t_to_date)
        cnt_c_week_incoming_afterhour = getCountOfAfterHour(c_week_incoming_list,
                                                            agent_obj.open_weekly_from,
                                                            agent_obj.open_weekly_to,
                                                            agent_obj.open_sat_from,
                                                            agent_obj.open_sat_to)
        # print("HHHH")
        data = {
            "cnt_incoming": len(incoming_list),
            "cnt_incoming_afterhour": cnt_incoming_afterhour,
            "cnt_scheduling_afterhour": cnt_scheduling_afterhour,
            "cnt_booked": len(booked_list),
            "cnt_booked_afterhour": cnt_booked_afterhour,
            "cnt_l_week_incoming_afterhour": cnt_l_week_incoming_afterhour,
            "cnt_c_week_incoming_afterhour": cnt_c_week_incoming_afterhour
        }
        # print("HHHH")
        # print(data)


        return data
    except Exception as e:
        return None


# ***********************************************************************************
# @Function: Get Booking Chart Data
# @Return: Booking Chart Data
# -----------------------------------------------------------------------------------
def getBookingChartData(user_email, agent_id, from_date, to_date, period_id):
    try:
        res = []
        data_dict = {}
        agent_obj = tbl_agent.objects.get(id=agent_id)
        agent_code = agent_obj.code
        booked_list = callEventListApi("scheduleCompleteAutoServ", agent_code, from_date, to_date)
        # print(booked_list)
        # print(period_id,"period_id")
        if from_date == to_date:
            for i in range(0, 12):
                key = str(i*2) + "h - " + str((i+1)*2) + "h"
                data_dict[key] = 0
            for booked in booked_list:
                time_obj = datetime.datetime.strptime(booked["Date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                hour = time_obj.hour
                if hour % 2 == 0:
                    key = str(hour) + "h - " + str(hour+2) + "h"
                else:
                    key = str(hour-1) + "h - " + str(hour+1) + "h"
                data_dict[key] += 1

        elif period_id != 4:
            for i in range(0, (to_date-from_date).days + 1):
                date = from_date + timedelta(days=i)
                data_dict[atsd_basic.date2Str(date)] = 0
            for booked in booked_list:
                # print(booked["Date"])
                time_obj = datetime.datetime.strptime(booked["Date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                data_dict[atsd_basic.date2Str(time_obj)] += 1

        elif period_id == 4:
            sunday_list = []
            first_sunday = atsd_basic.nextWeekday(from_date, 6)
            if (first_sunday - from_date).days > 3:
                first_sunday = atsd_basic.nextWeekday(first_sunday, 6)
            sunday_list.append(first_sunday)
            sunday_list.append(atsd_basic.nextWeekday(sunday_list[0] + timedelta(days=1), 6))
            sunday_list.append(atsd_basic.nextWeekday(sunday_list[1] + timedelta(days=1), 6))
            forth_sunday = atsd_basic.nextWeekday(sunday_list[2] + timedelta(days=1), 6)
            if (to_date - forth_sunday).days > 3:
                sunday_list.append(forth_sunday)
                sunday_list.append(to_date)
            else:
                sunday_list.append(to_date)

            if len(sunday_list) == 4:
                key_ary = ["1st Week", "2nd Week", "3rd Week", "4th Week"]
            elif len(sunday_list) == 5:
                key_ary = ["1st Week", "2nd Week", "3rd Week", "4th Week", "5th Week"]

            for key in key_ary:
                data_dict[key] = 0

            for booked in booked_list:
                time_obj = datetime.datetime.strptime(booked["Date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                day = time_obj.day
                for i in range(0, len(sunday_list)+1):
                    if day <= sunday_list[i].day:
                        data_dict[key_ary[i]] += 1
                        break
        # elif period_id == 5:
        #     res.append({
        #         "x-axis": 2021-11-18,
        #         "value": 2
        #
        #     })
        # return res
        # print(data_dict,"dict is here")
        for date, value in data_dict.items():
            res.append({
                "x-axis": date,
                "value": value
            })
        # print(res,"here is result")
        return res

    except Exception as e:
        return None



# --------------------------------- Report 2 --------------------------------- #

# ***********************************************************************************
# @Function: Get Campaign Indicator Data
# @Return: Campaign Indicator Data
# -----------------------------------------------------------------------------------
def getCampaignIndicatorData(user_email, agent_id, from_date, to_date, period_id, campaign_name):
    try:
        agent_obj = tbl_agent.objects.get(id=agent_id)
        agent_code = agent_obj.code

        campaign_list = callEventListApi("classes", agent_code, from_date, to_date)
        if campaign_list == None:
            return None
        cnt_total_campaign = 0
        cnt_active_campaign = 0

        campaign_ary = [""]

        for campaign in campaign_list:
            try:
                s_campaign_name = campaign["eventInfoStr1"].split(":")[0]
                s_campaign_status = campaign["eventInfoStr1"].split(":")[1]

                if s_campaign_name not in campaign_ary:
                    campaign_ary.append(campaign["eventInfoStr1"].split(":")[0])

                if campaign_name != "" and s_campaign_name != campaign_name:
                    continue
                cnt_total_campaign += 1
                if s_campaign_status == "STARTED":
                    cnt_active_campaign += 1

            except Exception:
                continue

        cnt_sms_sent = callEventCountApi("rentStarted", agent_code, from_date, to_date)
        cnt_sms_booked = callEventCountApi("timeSelected", agent_code, from_date, to_date)
        if cnt_sms_sent == None or cnt_sms_booked == None:
            return None

        data = {
            "campaign_ary": campaign_ary,
            "cnt_total_campaign": cnt_total_campaign,
            "cnt_active_campaign": cnt_active_campaign,
            "cnt_sms_sent": cnt_sms_sent,
            "cnt_sms_booked": cnt_sms_booked
        }
        return data
    except Exception as e:
        return None

# ***********************************************************************************
# @Function: Get Sms Sent Chart Data
# @Return: Sms Sent Chart Data
# -----------------------------------------------------------------------------------
def getSmsSentChartData(user_email, agent_id, from_date, to_date, period_id, campaign_name=""):
    try:
        res = []
        data_dict = {}
        agent_obj = tbl_agent.objects.get(id=agent_id)
        agent_code = agent_obj.code

        event_list = callEventListApi("rentStarted", agent_code, from_date, to_date)

        if from_date == to_date:
            for i in range(0, 12):
                key = str(i*2) + "h - " + str((i+1)*2) + "h"
                data_dict[key] = 0
            for event in event_list:
                if campaign_name != "" and (event["eventInfoStr1"] == None or event["eventInfoStr1"].split(":")[0] != campaign_name):
                    continue
                time_obj = datetime.datetime.strptime(event["Date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                hour = time_obj.hour
                if hour % 2 == 0:
                    key = str(hour) + "h - " + str(hour+2) + "h"
                else:
                    key = str(hour-1) + "h - " + str(hour+1) + "h"
                data_dict[key] += 1

        elif period_id != 4:
            for i in range(0, (to_date-from_date).days + 1):
                date = from_date + timedelta(days=i)
                data_dict[atsd_basic.date2Str(date)] = 0
            for event in event_list:
                if campaign_name != "" and (event["eventInfoStr1"] == None or event["eventInfoStr1"].split(":")[0] != campaign_name):
                    continue
                time_obj = datetime.datetime.strptime(event["Date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                data_dict[atsd_basic.date2Str(time_obj)] += 1

        elif period_id == 4:
            sunday_list = []
            first_sunday = atsd_basic.nextWeekday(from_date, 6)
            if (first_sunday - from_date).days > 3:
                first_sunday = atsd_basic.nextWeekday(first_sunday, 6)
            sunday_list.append(first_sunday)
            sunday_list.append(atsd_basic.nextWeekday(sunday_list[0] + timedelta(days=1), 6))
            sunday_list.append(atsd_basic.nextWeekday(sunday_list[1] + timedelta(days=1), 6))
            forth_sunday = atsd_basic.nextWeekday(sunday_list[2] + timedelta(days=1), 6)
            if (to_date - forth_sunday).days > 3:
                sunday_list.append(forth_sunday)
                sunday_list.append(to_date)
            else:
                sunday_list.append(to_date)

            if len(sunday_list) == 4:
                key_ary = ["1st Week", "2nd Week", "3rd Week", "4th Week"]
            elif len(sunday_list) == 5:
                key_ary = ["1st Week", "2nd Week", "3rd Week", "4th Week", "5th Week"]

            for key in key_ary:
                data_dict[key] = 0

            for event in event_list:
                if campaign_name != "" and (event["eventInfoStr1"] == None or event["eventInfoStr1"].split(":")[0] != campaign_name):
                    continue
                time_obj = datetime.datetime.strptime(event["Date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                day = time_obj.day
                for i in range(0, len(sunday_list)+1):
                    if day <= sunday_list[i].day:
                        data_dict[key_ary[i]] += 1
                        break

        for date, value in data_dict.items():
            res.append({
                "x-axis": date,
                "value": value
            })
        return res

    except Exception as e:
        return None


# ***********************************************************************************
# @Function: Get Sms Booked Chart Data
# @Return: Sms Sent Booked Data
# -----------------------------------------------------------------------------------
def getSmsBookedChartData(user_email, agent_id, from_date, to_date, period_id, campaign_name=""):
    try:
        res = []
        data_dict = {}
        agent_obj = tbl_agent.objects.get(id=agent_id)
        agent_code = agent_obj.code

        event_list = callEventListApi("timeSelected", agent_code, from_date, to_date)

        if from_date == to_date:
            for i in range(0, 12):
                key = str(i*2) + "h - " + str((i+1)*2) + "h"
                data_dict[key] = 0
            for event in event_list:
                if campaign_name != "" and (event["eventInfoStr1"] == None or event["eventInfoStr1"].split(":")[0] != campaign_name):
                    continue
                time_obj = datetime.datetime.strptime(event["Date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                hour = time_obj.hour
                if hour % 2 == 0:
                    key = str(hour) + "h - " + str(hour+2) + "h"
                else:
                    key = str(hour-1) + "h - " + str(hour+1) + "h"
                data_dict[key] += 1

        elif period_id != 4:
            for i in range(0, (to_date-from_date).days + 1):
                date = from_date + timedelta(days=i)
                data_dict[atsd_basic.date2Str(date)] = 0
            for event in event_list:
                if campaign_name != "" and (event["eventInfoStr1"] == None or event["eventInfoStr1"].split(":")[0] != campaign_name):
                    continue
                time_obj = datetime.datetime.strptime(event["Date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                data_dict[atsd_basic.date2Str(time_obj)] += 1

        elif period_id == 4:
            sunday_list = []
            first_sunday = atsd_basic.nextWeekday(from_date, 6)
            if (first_sunday - from_date).days > 3:
                first_sunday = atsd_basic.nextWeekday(first_sunday, 6)
            sunday_list.append(first_sunday)
            sunday_list.append(atsd_basic.nextWeekday(sunday_list[0] + timedelta(days=1), 6))
            sunday_list.append(atsd_basic.nextWeekday(sunday_list[1] + timedelta(days=1), 6))
            forth_sunday = atsd_basic.nextWeekday(sunday_list[2] + timedelta(days=1), 6)
            if (to_date - forth_sunday).days > 3:
                sunday_list.append(forth_sunday)
                sunday_list.append(to_date)
            else:
                sunday_list.append(to_date)

            if len(sunday_list) == 4:
                key_ary = ["1st Week", "2nd Week", "3rd Week", "4th Week"]
            elif len(sunday_list) == 5:
                key_ary = ["1st Week", "2nd Week", "3rd Week", "4th Week", "5th Week"]

            for key in key_ary:
                data_dict[key] = 0

            for event in event_list:
                if campaign_name != "" and (event["eventInfoStr1"] == None or event["eventInfoStr1"].split(":")[0] != campaign_name):
                    continue
                time_obj = datetime.datetime.strptime(event["Date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                day = time_obj.day
                for i in range(0, len(sunday_list)+1):
                    if day <= sunday_list[i].day:
                        data_dict[key_ary[i]] += 1
                        break

        for date, value in data_dict.items():
            res.append({
                "x-axis": date,
                "value": value
            })
        return res

    except Exception as e:
        return None


# --------------------------------- Report 3 --------------------------------- #

# ***********************************************************************************
# @Function: Get Voice Mail, Average Response Time Chart Data
# @Return: Voice Mail, Average Response Time Chart Data
# -----------------------------------------------------------------------------------
def getvmAndArtChartData(user_email, v_m_agent_list, from_date, to_date, period_id):
    try:
        print("hello")
        data_vm_chart = []
        data_art_chart = []

        vm_event_dict = {}
        linked_event_dict = {}

        sunday_list = []
        # print("vmand art chart")
        for agent in v_m_agent_list:
            # print(agent["code"])
            event_list = callEventListApi("voiceMail", agent["code"], from_date - timedelta(days=7), to_date)
            print(event_list)

            # print()
            vm_event_dict[str(agent["id"])] = []

            if event_list != None:
                vm_event_dict[str(agent["id"])] = event_list

            event_list = callEventListApi("linkClicked", agent["code"], from_date, to_date)

            print(event_list)

            linked_event_dict[str(agent["id"])] = []
            if event_list != None:
                linked_event_dict[str(agent["id"])] = event_list
            # print("not worry")
        # --------------- get date key array --------------- #
        date_key_ary = []
        for i in range(0, (to_date - from_date).days + 1):
            date = from_date + timedelta(days=i)

            date_key_ary.append(atsd_basic.date2Str(date))

        # --------------- get voice mail chart data --------------- #
        tmp_res = {}

        # print('tarsem')
        # print(date_key_ary)
        # print('tushar')

        for date_key in date_key_ary:
            tmp_res[date_key] = {
                "Total": 0,
                "Last Period": 0,
            }
            # print(tmp_res,"here is eror")
            for agent in v_m_agent_list:
                event_count = 0
                last_period_event_count = 0
                for event in vm_event_dict[str(agent["id"])]:
                    time_obj = datetime.datetime.strptime(event["Date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    # print(time_obj,'timeobj')
                    key = atsd_basic.date2Str(time_obj)

                    print('tarsem')
                    print(date_key)
                    print('tushar')

                    if key == date_key:
                        event_count += 1

                    str_last = atsd_basic.date2Str(datetime.datetime.strptime(date_key, "%Y-%m-%d").date() - timedelta(days=7))
                    print('tarsem1')
                    print(str_last)
                    print('tushar1')
                    if key == str_last:
                        last_period_event_count += 1
                # print("date is changed")
                tmp_res[date_key][agent["name"]] = event_count
                tmp_res[date_key]["Total"] += event_count
                tmp_res[date_key]["Last Period"] += last_period_event_count
                # print(tmp_res)

        idx = 0
        for key, value in tmp_res.items():
            data_vm_chart.append(value)
            data_vm_chart[idx]["date"] = key
            idx += 1
        # print(idx,"idx")
        # --------------- get average response time chart data --------------- #
        tmp_res = {}
        # print(date_key_ary)
        # print('jjj')
        # print(v_m_agent_list)
        # print('here')
        for date_key in date_key_ary:
            tmp_res[date_key] = {}
            print(tmp_res)
            print('mandeep')
            for agent in v_m_agent_list:
                vm_event_time_list = []
                linked_event_time_list = []
                # ---------- extract event in the range period ---------- #
                for event in vm_event_dict[str(agent["id"])]:
                    print(event)
                    print('here')
                    time_obj = datetime.datetime.strptime(event["Date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    print(time_obj)
                    print('date')
                    key = atsd_basic.date2Str(time_obj)
                    # print(key)
                    print(date_key)
                    if key != date_key:
                        print("key")
                        continue

                    flag = True
                    for i in range(0, len(vm_event_time_list)):
                        if vm_event_time_list[i]["phone_number"] == event["phoneNum"] and (time_obj-vm_event_time_list[i]["Date"]).seconds < 3600:
                            flag = False
                            break
                    print("flag")
                    print(flag)
                    if flag == True:
                        vm_event_time_list.append({
                            "phone_number": event["phoneNum"],
                            "Date": time_obj,
                        })

                # ---------- extract event in the range period ---------- #
                for event in linked_event_dict[str(agent["id"])]:
                    print(event)
                    time_obj = datetime.datetime.strptime(event["Date"], "%Y-%m-%dT%H:%M:%S.%fZ")
                    key = atsd_basic.date2Str(time_obj)
                    print(key)
                    if key != date_key:

                        continue

                    linked_event_time_list.append({
                        "phone_number": event["phoneNum"],
                        "Date": time_obj
                    })
                    print(linked_event_time_list,"working")
                # ---------- calculate response time ---------- #
                sum_response_time = 0
                response_cnt = 0

                flag_ary = []
                for vm_event_time in vm_event_time_list:
                    for i in range(0, len(linked_event_time_list)):
                        if i in flag_ary:
                            continue
                        if linked_event_time_list[i]["phone_number"] != vm_event_time["phone_number"]:
                            continue
                        print("time")
                        response_time = (linked_event_time_list[i]["Date"] - vm_event_time["Date"]).seconds
                        print(response_time)
                        print("responce")
                        if response_time >= 3600:
                            continue
                        sum_response_time += response_time
                        response_cnt += 1
                        flag_ary.append(i)
                        break

                tmp_res[date_key][agent["name"]] = 0
                if response_cnt != 0:
                    tmp_res[date_key][agent["name"]] = sum_response_time / response_cnt

        idx = 0
        for key, value in tmp_res.items():
            data_art_chart.append(value)
            data_art_chart[idx]["date"] = key
            idx += 1
        print("done")
        return data_vm_chart, data_art_chart

    except Exception as e:
        print("not is done")
        return None, None


# --------------------------------- Report 3 --------------------------------- #
# ***********************************************************************************
# @Function: Get Voice Mail List
# @Return: VoiceMail List
# -----------------------------------------------------------------------------------
def getVoiceMailList(user_email, from_date=None, to_date=None, message=None, status=None, type=None):
    try:
        user_obj = tbl_user.objects.get(email=user_email)
        # print(user_obj)

        voicemail_obj_list = list(tbl_voicemail.objects.all().order_by("-time"))
        # print(voicemail_obj_list)
        voicemail_list = []
        for voicemail_obj in voicemail_obj_list:
            # print(voicemail_obj.advisor_phone)
            advisor_phone = voicemail_obj.advisor_phone
            advisor = atsd_basic.getAdvisorByPhoneNumber(advisor_phone)

            # print(advisor)
            if advisor == None:
                continue
            user_advisor_list = user_obj.advisors.split(",")
            print(advisor["id"])
            print(user_advisor_list)
            if str(advisor["id"]) not in user_advisor_list:
            # if advisor["id"] not in user_advisor_list:
                continue
                # print('if')

            # print("HHHH")
            # print(voicemail_obj.time.year, "here")

            voicemail_time = datetime.datetime(voicemail_obj.time.year, voicemail_obj.time.month,
                                               voicemail_obj.time.day,
                                               voicemail_obj.time.hour, voicemail_obj.time.minute,
                                               voicemail_obj.time.second)

            # print(voicemail_time)
            # ---------- get all message list ---------- #
            message_list = [{
                "sender": "Caller",
                "message": voicemail_obj.message,
                "time": voicemail_obj.time
            }]
            response_list = list(tbl_voicemail_response.objects.filter(vm_id=voicemail_obj.id))
            for response in response_list:
                message_list.append({
                    "sender": response.replier_name,
                    "message": response.message,
                    "time": response.time
                })

            for i in range(0, len(message_list)):
                for j in range(i+1, len(message_list)):
                    if (message_list[i]["time"] < message_list[j]["time"]):
                        tmp = message_list[i]
                        message_list[i] = message_list[j]
                        message_list[j] = tmp

            for mes in message_list:
                mes["time"] = mes["time"].strftime("%Y-%m-%d %H:%M:%S")

            # --------------- filter data --------------- #
            if from_date != None and voicemail_time < datetime.datetime.strptime(from_date, "%Y-%m-%d"):
                continue
            if to_date != None and voicemail_time > datetime.datetime.strptime(to_date, "%Y-%m-%d") + datetime.timedelta(days=1):
                continue

            if message != None:
                flg = False
                for mes in message_list:
                    if mes["message"].find(message) != -1:
                        flg = True
                        break
                if flg == False:
                    continue

            if status != None:
                if status == 1 and voicemail_obj.status != 0 and voicemail_obj.status != 1:
                    continue
                if voicemail_obj.status != status:
                    continue
            elif voicemail_obj.status == 3:
                continue

            if type != None and voicemail_obj.type != type:
                continue
            # print("HHHHHJH")
            voicemail_list.append({
                    "id": voicemail_obj.id,
                "message_list": message_list,
                "caller_phone": voicemail_obj.caller_phone,
                "advisor_phone": voicemail_obj.advisor_phone,
                "caller_name": voicemail_obj.caller_name,
                "ok_text": voicemail_obj.ok_text,
                "type": voicemail_obj.type,
                "status": voicemail_obj.status,
                "flag": voicemail_obj.flag,
                "caller_replied": voicemail_obj.caller_replied,
                "time": str(voicemail_time)
            })

        return voicemail_list

    except Exception as e:
        return None