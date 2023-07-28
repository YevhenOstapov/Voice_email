import json
import math

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from autoservices.database.models import *
from autoservices.module.glb.constant.http_ret_code import *
from autoservices.module.atsd.constant.ret_code import *
from autoservices.module.atsd import auth as atsd_auth
from autoservices.module.atsd import basic as atsd_basic
from autoservices.module.atsd import user as atsd_user


# ***********************************************************************************
# @Function: Index View
# -----------------------------------------------------------------------------------
@login_required
def indexView(request, template_name="adminpanel/index.html"):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)



        if user_obj.is_superuser == 0:
            return redirect("/")
        password = user_obj.s_password


        user_list = atsd_user.getCustomerList(email, "")
        total_user = len(user_list)
        total_page = math.ceil(total_user / 15)
        user_list = user_list[0:15]



        agent_list = atsd_user.getAgentList()
        advisor_list = atsd_basic.getAdvisorList()
        company_list = atsd_basic.getCompanyList()

        data = {
            "email": email,
            "password": password,
            "user_list": user_list,
            "total_user": total_user,
            "total_page": total_page,

            "agent_list": agent_list,
            "advisor_list": advisor_list,
            "company_list": company_list
        }
        return render(request, template_name, data)
    except Exception as e:
        return redirect("/")


# ***********************************************************************************
# @Function: Agent View
# -----------------------------------------------------------------------------------
@login_required
def agentView(request, template_name="adminpanel/agent.html"):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return redirect("/")
        password = user_obj.s_password

        agent_list = atsd_user.getAgentList()
        total_agent = len(agent_list)
        total_page = math.ceil(total_agent / 15)
        agent_list = agent_list[0:15]

        data = {
            "email": email,
            "password": password,
            "agent_list": agent_list,
            "total_agent": total_agent,
            "total_page": total_page
        }

        return render(request, template_name, data)

    except Exception as e:
        return redirect("/")


# ***********************************************************************************
# @Function: Get Page Users
# -----------------------------------------------------------------------------------
@login_required
def getPageUsers(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        filter_str = request.POST["filter_str"]
        cur_page = int(request.POST["cur_page"])
        user_list = atsd_user.getCustomerList(email, filter_str)
        total_user = len(user_list)
        total_page = math.ceil(total_user / 15)
        user_list = user_list[15 * (cur_page - 1):15 * cur_page]
        data = {
            "total_page": total_page,
            "total_user": total_user,
            "user_list": user_list
        }
        return HttpResponse(json.dumps(data))

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Get Page Agents
# -----------------------------------------------------------------------------------
@login_required
def getPageAgents(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        filter_str = request.POST["filter_str"]
        cur_page = int(request.POST["cur_page"])
        agent_list = atsd_user.getAgentList(filter_str)
        total_agent = len(agent_list)
        total_page = math.ceil(total_agent / 15)
        agent_list = agent_list[15 * (cur_page - 1):15 * cur_page]
        data = {
            "total_page": total_page,
            "total_agent": total_agent,
            "agent_list": agent_list
        }
        return HttpResponse(json.dumps(data))

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Register User
# -----------------------------------------------------------------------------------
@login_required
def registerUser(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        data = json.loads(request.POST["param"])
        ret_code, user_obj = atsd_auth.registerUser(data["email"], data["first_name"],
                                                    data["last_name"], data["phone_number"],
                                                    data["company_id"],
                                                    data["factor_booked"], data["factor_transfer"],
                                                    ",".join(map(str, data["agents"])),
                                                    ",".join(map(str, data["advisors"])),
                                                    json.dumps(data["reports"]))
        if ret_code == REG_EXISTING_EMAIL:
            return HttpResponse("existing_email", status=HttpResponse500)
        return HttpResponse(user_obj.uid)

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Update User
# -----------------------------------------------------------------------------------
@login_required
def updateUser(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        data = json.loads(request.POST["param"])
        user_obj = tbl_user.objects.get(email=data["email"])
        user_obj.first_name = data["first_name"]
        user_obj.last_name = data["last_name"]
        user_obj.phone_number = data["phone_number"]
        user_obj.company_id = data["company_id"]
        user_obj.factor_booked = data["factor_booked"]
        user_obj.factor_transfer = data["factor_transfer"]
        user_obj.agents = ",".join(map(str, data["agents"]))
        user_obj.advisors = ",".join(map(str, data["advisors"]))
        user_obj.reports = json.dumps(data["reports"])
        user_obj.save()
        return HttpResponse("success")

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Delete User
# -----------------------------------------------------------------------------------
@login_required
def deleteUser(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        uid = int(request.POST["uid"])
        user_obj = tbl_user.objects.get(uid=uid)
        user_obj.delete()
        return HttpResponse("success")

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Register Agent
# -----------------------------------------------------------------------------------
@login_required
def registerAgent(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        data = json.loads(request.POST["param"])
        agent_id = atsd_user.registerAgent(data["name"], data["code"], data["type"],
                                           data["open_weekly_from"], data["open_weekly_to"], data["open_sat_from"],
                                           data["open_sat_to"])
        if agent_id == None:
            return HttpResponse("error", status=HttpResponse500)
        if agent_id == -1:
            return HttpResponse("existing_name", status=HttpResponse500)

        return HttpResponse(agent_id)

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Update Agent
# -----------------------------------------------------------------------------------
@login_required
def updateAgent(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        data = json.loads(request.POST["param"])
        agent_obj = tbl_agent.objects.get(code=data["code"])
        agent_obj.name = data["name"]
        agent_obj.type = data["type"]
        agent_obj.open_weekly_from = data["open_weekly_from"]
        agent_obj.open_weekly_to = data["open_weekly_to"]
        agent_obj.open_sat_from = data["open_sat_from"]
        agent_obj.open_sat_to = data["open_sat_to"]
        agent_obj.save()
        return HttpResponse("success")

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Delete Agent
# -----------------------------------------------------------------------------------
@login_required
def deleteAgent(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        id = int(request.POST["id"])

        # ---------- delete agent from user ---------- #
        user_obj_list = list(tbl_user.objects.all())
        for user_obj in user_obj_list:
            agent_id_list = user_obj.agents.split(",")
            if str(id) in agent_id_list:
                agent_id_list.remove(str(id))
                user_obj.agents = ",".join(agent_id_list)
                user_obj.save()

        agent_obj = tbl_agent.objects.get(id=id)
        agent_obj.delete()

        return HttpResponse("success")

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Company View
# -----------------------------------------------------------------------------------
def companyView(request, template_name="adminpanel/company.html"):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return redirect("/")
        password = user_obj.s_password

        company_list = atsd_basic.getCompanyList()
        total_company = len(company_list)
        total_page = math.ceil(total_company / 15)
        company_list = company_list[0:15]

        data = {
            "email": email,
            "password": password,
            "company_list": company_list,
            "total_company": total_company,
            "total_page": total_page
        }

        return render(request, template_name, data)

    except Exception as e:
        return redirect("/")


# ***********************************************************************************
# @Function: Get Page Company
# -----------------------------------------------------------------------------------
@login_required
def getPageCompany(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        filter_str = request.POST["filter_str"]
        cur_page = int(request.POST["cur_page"])
        company_list = atsd_basic.getCompanyList(filter_str)
        total_company = len(company_list)
        total_page = math.ceil(total_company / 15)
        company_list = company_list[15 * (cur_page - 1):15 * cur_page]
        data = {
            "total_page": total_page,
            "total_company": total_company,
            "company_list": company_list
        }
        return HttpResponse(json.dumps(data))

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Register Company
# -----------------------------------------------------------------------------------
@login_required
def registerCompany(request):

    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        data = json.loads(request.POST["param"])
        print(data,'h2')
        company_id = atsd_basic.registerCompany(data["name"], data["group"], data["twilio_account_sid"],
                                                data["twilio_auth_token"], data["twilio_phone_number"], data["customerInfoAPI"],
                                                data["fallbackForwardTo"],data["unregisteredForwardTo"],data["unregisteredEmailTo"],
                                                data["unregisteredSmsTo"],data["unregisteredAPICall"])
        if company_id == None:
            return HttpResponse("error", status=HttpResponse500)
        if company_id == -1:
            return HttpResponse("existing_name", status=HttpResponse500)

        return HttpResponse(company_id)

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Update Company
# -----------------------------------------------------------------------------------
@login_required
def updateCompany(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        data = json.loads(request.POST["param"])
        company_obj = tbl_company.objects.get(name=data["name"])
        company_obj.group = data["group"]
        company_obj.twilio_account_sid = data["twilio_account_sid"]
        company_obj.twilio_auth_token = data["twilio_auth_token"]
        company_obj.twilio_phone_number = data["twilio_phone_number"]
        company_obj.customerInfoAPI = data["customerInfoAPI"]
        company_obj.fallbackForwardTo = data["fallbackForwardTo"]
        company_obj.unregisteredForwardTo = data["unregisteredForwardTo"]
        company_obj.unregisteredEmailTo = data["unregisteredEmailTo"]
        company_obj.unregisteredSmsTo = data["unregisteredSmsTo"]
        company_obj.unregisteredAPICall = data["unregisteredAPICall"]
        company_obj.save()
        return HttpResponse("success")

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Delete Company
# -----------------------------------------------------------------------------------
@login_required
def deleteCompany(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        id = int(request.POST["id"])
        company_obj = tbl_company.objects.get(id=id)
        company_obj.delete()

        return HttpResponse("success")

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Advisor View
# -----------------------------------------------------------------------------------
def advisorView(request, template_name="adminpanel/advisor.html"):
    try:

        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return redirect("/")
        password = user_obj.s_password

        advisor_list = atsd_basic.getAdvisorList()
        total_advisor = len(advisor_list)
        total_page = math.ceil(total_advisor / 15)
        advisor_list = advisor_list[0:15]
        company_list = atsd_basic.getCompanyList()
        data = {
            "email": email,
            "password": password,
            "advisor_list": advisor_list,
            "total_advisor": total_advisor,
            "total_page": total_page,
            "company_list": company_list
        }

        return render(request, template_name, data)

    except Exception as e:

        return redirect("/")


# ***********************************************************************************
# @Function: Get Page Advisor
# -----------------------------------------------------------------------------------
@login_required
def getPageAdvisor(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        filter_str = request.POST["filter_str"]
        cur_page = int(request.POST["cur_page"])
        advisor_list = atsd_basic.getAdvisorList(filter_str)
        total_advisor = len(advisor_list)
        total_page = math.ceil(total_advisor / 15)
        advisor_list = advisor_list[15 * (cur_page - 1):15 * cur_page]
        data = {
            "total_page": total_page,
            "total_advisor": total_advisor,
            "advisor_list": advisor_list
        }
        return HttpResponse(json.dumps(data))

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Register Advisor
# -----------------------------------------------------------------------------------
@login_required
def registerAdvisor(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        data = json.loads(request.POST["param"])

        advisor_id = atsd_basic.registerAdvisor(data)
        if advisor_id == None:
            return HttpResponse("error", status=HttpResponse500)
        if advisor_id == -1:
            return HttpResponse("existing_name", status=HttpResponse500)

        return HttpResponse(advisor_id)

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Update Advisor
# -----------------------------------------------------------------------------------
@login_required
def updateAdvisor(request):
    try:

        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        data = json.loads(request.POST["param"])

        ret_code = atsd_basic.updateAdvisor(data["name"], data)
        if ret_code == False:

            return HttpResponse("error", status=HttpResponse500)
        return HttpResponse("success")
    except Exception as e:

        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Delete Advisor
# -----------------------------------------------------------------------------------
@login_required
def deleteAdvisor(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        if user_obj.is_superuser == 0:
            return HttpResponse("error", status=HttpResponse500)

        name = request.POST["name"]
        advisor_obj = tbl_advisor.objects.get(name=name)
        advisor_obj.delete()

        return HttpResponse("success")

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)
