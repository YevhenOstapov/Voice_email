# ***********************************************************************************
# File Name: user.py
# Author: Dimitar
# Created: 2020-02-21
# Description: User Module For autoservices
# -----------------------------------------------------------------------------------

import json

from autoservices.database.models import *
from autoservices.module.atsd.constant.project import *
from autoservices.module.atsd import basic as atsd_basic

# ***********************************************************************************
# @Function: Get Customer List
# @Return: Customer List
# -----------------------------------------------------------------------------------
def getCustomerList(except_email, filter_str):
    try:
        user_list = list(tbl_user.objects.filter().exclude(email=except_email))
        res = []
        for user in user_list:
            try:
                flg = False
                if user.email.find(filter_str) != -1:
                    flg = True
                if user.first_name.find(filter_str) != -1:
                    flg = True
                if user.last_name.find(filter_str) != -1:
                    flg = True
                if user.phone_number.find(filter_str) != -1:
                    flg = True

                if flg == False:
                    continue

                try:
                    agents = list(map(int, user.agents.split(",")))
                except Exception as e1:
                    agents = []

                try:
                    advisors = list(map(int, user.advisors.split(",")))
                except Exception as e1:
                    advisors = []

                company_name = ""
                company = atsd_basic.getCompanyById(user.company_id)
                if company != None:
                    company_name = company["name"]

                res.append({
                    "id": user.id,
                    "uid": user.uid,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone_number": user.phone_number,
                    "company_id": user.company_id,
                    "company_name": company_name,
                    "factor_booked": user.factor_booked,
                    "factor_transfer": user.factor_transfer,
                    "agents": agents,
                    "advisors": advisors,
                    "reports": json.loads(user.reports)
                })

            except Exception as e1:
                continue

        return res

    except Exception as e:
        return []


# ***********************************************************************************
# @Function: Get Agent List
# @Return: Agent List
# -----------------------------------------------------------------------------------
def getAgentList(filter_str=""):
    try:
        agent_list = list(tbl_agent.objects.filter())
        res = []
        for agent in agent_list:
            try:
                flg = False
                if agent.name.find(filter_str) != -1:
                    flg = True

                if flg == False:
                    continue

                res.append({
                    "id": agent.id,
                    "name": agent.name,
                    "code": agent.code,
                    "type": agent.type,
                    "type_name": AGENT_TYPE[agent.type - 1],
                    "open_weekly_from": agent.open_weekly_from,
                    "open_weekly_to": agent.open_sat_to,
                    "open_sat_from": agent.open_sat_from,
                    "open_sat_to": agent.open_sat_to
                })

            except Exception:
                continue

        return res
    except Exception as e:
        return []


# ***********************************************************************************
# @Function: Get Agent By Id
# @Return: Agent Object
# -----------------------------------------------------------------------------------
def getAgentById(agent_id):
    try:
        agent_list = getAgentList()
        for agent in agent_list:
            if agent["id"] == agent_id:
                return agent
        return None
    except Exception as e:
        return None


# ***********************************************************************************
# @Function: Register Agent
# @Return: Agent Id
# -----------------------------------------------------------------------------------
def registerAgent(name, code, type, open_weekly_from, open_weekly_to, open_sat_from, open_sat_to):
    try:
        agent_obj = tbl_agent()
        if len(list(tbl_agent.objects.filter(name=name))) > 0:
            return -1
        agent_obj.name = name
        agent_obj.code = code
        agent_obj.type = type
        agent_obj.open_weekly_from = open_weekly_from
        agent_obj.open_weekly_to = open_weekly_to
        agent_obj.open_sat_from = open_sat_from
        agent_obj.open_sat_to = open_sat_to
        agent_obj.save()
        return agent_obj.id
    except Exception as e:
        return None