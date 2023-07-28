import math
import time
import json
import requests
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from autoservices.database.models import *
from autoservices.module.glb.constant.http_ret_code import *
from autoservices.module.glb import twilio as glb_twilio
from autoservices.module.atsd.constant.project import *
from autoservices.module.atsd import basic as atsd_basic
from autoservices.module.atsd import user as atsd_user
from autoservices.module.atsd import report as atsd_report

# ***********************************************************************************
# @Function: Index View
# -----------------------------------------------------------------------------------
@login_required
def indexView(request, template_name="userpanel/index.html"):
    
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        report_list = json.loads(user_obj.reports)

        if len(report_list) == 0:
            data = {
                "uid": user_obj.uid,
                "email": user_obj.email,
                "password": user_obj.s_password,
                "first_name": user_obj.first_name,
                "last_name": user_obj.last_name,
                "phone_number": user_obj.phone_number,

                "report_list": report_list
            }
        
            return render(request, template_name, data)

        if report_list[0]["type"] == 100:
            return redirect("/user/faq")
        else:
            return redirect("/user/report/0")

    except Exception as e:
        return render(request, template_name)


# ***********************************************************************************
# @Function: Faq View
# -----------------------------------------------------------------------------------
@login_required
def faqView(request, template_name="userpanel/faq.html"):
    email = request.session.get("email")
    user_obj = tbl_user.objects.get(email=email)
    report_list = json.loads(user_obj.reports)

    report_id = 10000

    data = {
        "uid": user_obj.uid,
        "email": user_obj.email,
        "password": user_obj.s_password,
        "first_name": user_obj.first_name,
        "last_name": user_obj.last_name,
        "phone_number": user_obj.phone_number,

        "report_list": report_list,
        "report_id": report_id
    }
    return render(request, template_name, data)


# ***********************************************************************************
# @Function: Report View
# -----------------------------------------------------------------------------------
@login_required
def reportView(request, report_id, template_name1="userpanel/report1.html",
                                   template_name2="userpanel/report2.html",
                                   template_name3="userpanel/report3.html",
                                   template_name4="userpanel/report4.html",
                                   template_name_other = "userpanel/report_other.html"):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        report_list = json.loads(user_obj.reports)
        agent_id_list = list(map(int, user_obj.agents.split(",")))

        report_dict = report_list[report_id]
        report_name = report_dict["report_name"]
        report_url = report_dict["url"]
        report_agent_type = report_dict["type"]
        report_agent_list = []
        report_period_list = []

        for agent_id in agent_id_list:
            agent = atsd_user.getAgentById(agent_id)
            if agent == None:
                continue
            if agent["type"] == report_agent_type:
                report_agent_list.append(agent)

        for period in report_dict["period_type"]:
            report_period_list.append({
                "id": int(period),
                "name": PERIOD_TYPE[int(period)-1]
            })

        if len(report_period_list) == 0:
            report_period_list.append({
                "id": 3,
                "name": PERIOD_TYPE[2]
            })

        data = {
            "uid": user_obj.uid,
            "email": user_obj.email,
            "password": user_obj.s_password,
            "first_name": user_obj.first_name,
            "last_name": user_obj.last_name,
            "phone_number": user_obj.phone_number,

            "report_list": report_list,
            "report_name": report_name,
            "agent_list": report_agent_list,
            "period_list": report_period_list,
            "report_url": report_url,
            "report_id": report_id
        }
        
        if report_dict["type"] == 1:
            template_name = template_name1
        elif report_dict["type"] == 2:
            template_name = template_name2
        elif report_dict["type"] == 3:
            template_name = template_name3
        elif report_dict["type"] == 4:
            template_name = template_name4
        elif report_dict["type"] == 50:
            template_name = template_name_other

        return render(request, template_name, data)

    except Exception as e:
        return render(request, template_name1)


# ***********************************************************************************
# @Function: Get Report1 Data
# -----------------------------------------------------------------------------------
@login_required
def getReport1Data(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)

        agent_id = int(request.POST["agent_id"])
        period_id = int(request.POST["period_id"])
        agent_obj = tbl_agent.objects.get(id=agent_id)
        agent_code = agent_obj.code

        if period_id != 5:
            from_date, to_date = atsd_basic.getDatePeriodById(period_id)
        else:
            from_date = datetime.datetime.strptime(request.POST["from_date"], "%Y-%m-%d")
            to_date = datetime.datetime.strptime(request.POST["to_date"], "%Y-%m-%d")

        # if from_date == None:
          #  return HttpResponse("error", status=HttpResponse500)

        # -------------------- booked indicator -------------------- #
        data_b_i = atsd_report.getBookedIndicatorData(email, agent_id, from_date, to_date)
       # if data_b_i == None:
          #  return HttpResponse("error", status=HttpResponse500)

        # -------------------- afterhoour indicator -------------------- #
        data_ah_i = atsd_report.getAfterhourIndicatorData(email, agent_id, from_date, to_date)
      #  if data_ah_i == None:
          #  return HttpResponse("error", status=HttpResponse500)

        # -------------------- inbound indicator -------------------- #
        data_i_i = atsd_report.getInboundIndicatorData(email, agent_id, from_date, to_date)
       # if data_i_i == None:
          #  return HttpResponse("error", status=HttpResponse500)

        # -------------------- transfer indicator -------------------- #
        data_t_i = atsd_report.getTransferIndicatorData(email, agent_id, from_date, to_date)
       # if data_t_i == None:
          #  return HttpResponse("error", status=HttpResponse500)

        # -------------------- booking chart -------------------- #
        data_b_chart = atsd_report.getBookingChartData(email, agent_id, from_date, to_date, period_id)
       # if data_b_chart == None:
          #  return HttpResponse("error", status=HttpResponse500)
        try:
            data = {
                "cnt_scheduling":       data_b_i["cnt_scheduling"],
                "cnt_booked":           data_b_i["cnt_booked"],
                "cnt_transferred":      data_b_i["cnt_transferred"],
                "cnt_l_week_booked":    data_b_i["cnt_l_week_booked"],
                "cnt_c_week_booked":    data_b_i["cnt_c_week_booked"],

                "cnt_incoming_afterhour": data_ah_i["cnt_incoming_afterhour"],
                "cnt_scheduling_afterhour": data_ah_i["cnt_scheduling_afterhour"],
                "cnt_booked_afterhour": data_ah_i["cnt_booked_afterhour"],
                "cnt_l_week_incoming_afterhour": data_ah_i["cnt_l_week_incoming_afterhour"],
                "cnt_c_week_incoming_afterhour": data_ah_i["cnt_c_week_incoming_afterhour"],

                "cnt_incoming":         data_i_i["cnt_incoming"],
                "cnt_non_scheduling":   data_i_i["cnt_non_scheduling"],
                "cnt_l_week_incoming":  data_i_i["cnt_l_week_incoming"],
                "cnt_c_week_incoming":  data_i_i["cnt_c_week_incoming"],

                "cnt_operator_order":   data_t_i["cnt_operator_order"],
                "cnt_order":            data_t_i["cnt_order"],

                "data_b_chart":         data_b_chart,
            }
            return HttpResponse(json.dumps(data))
        except:
            return HttpResponse(json.dumps(data))

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Get Report2 Data
# -----------------------------------------------------------------------------------
@login_required
def getReport2Data(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)

        agent_id = int(request.POST["agent_id"])
        period_id = int(request.POST["period_id"])
        campaign_name = request.POST["campaign_name"]

        agent_obj = tbl_agent.objects.get(id=agent_id)
        agent_code = agent_obj.code

        if period_id != 5:
            from_date, to_date = atsd_basic.getDatePeriodById(period_id)
        else:
            from_date = datetime.datetime.strptime(request.POST["from_date"], "%Y-%m-%d")
            to_date = datetime.datetime.strptime(request.POST["to_date"], "%Y-%m-%d")

        if from_date == None:
            return HttpResponse("error", status=HttpResponse500)

        # -------------------- campaign indicator -------------------- #
        data_c_i = atsd_report.getCampaignIndicatorData(email, agent_id, from_date, to_date, period_id, campaign_name)

        # -------------------- sms sent chart -------------------- #
        data_ss_chart = atsd_report.getSmsSentChartData(email, agent_id, from_date, to_date, period_id, campaign_name)
        if data_ss_chart == None:
            return HttpResponse("error", status=HttpResponse500)

        # -------------------- sms booked chart -------------------- #
        data_sb_chart = atsd_report.getSmsBookedChartData(email, agent_id, from_date, to_date, period_id, campaign_name)
        if data_sb_chart == None:
            return HttpResponse("error", status=HttpResponse500)

        data = {
            "campaign_list": data_c_i["campaign_ary"],
            "cnt_total_campaign": data_c_i["cnt_total_campaign"],
            "cnt_active_campaign": data_c_i["cnt_active_campaign"],
            "cnt_sms_sent": data_c_i["cnt_sms_sent"],
            "cnt_sms_booked": data_c_i["cnt_sms_booked"],
            "data_ss_chart": data_ss_chart,
            "data_sb_chart": data_sb_chart
        }

        return HttpResponse(json.dumps(data))

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Get Report3 Data
# -----------------------------------------------------------------------------------
@login_required
def getReport3Data(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)

        agent_id = int(request.POST["agent_id"])
        period_id = int(request.POST["period_id"])

        agent_obj = tbl_agent.objects.get(id=agent_id)
        agent_code = agent_obj.code

        if period_id != 5:
            from_date, to_date = atsd_basic.getDatePeriodById(period_id)
        else:
            from_date = datetime.datetime.strptime(request.POST["from_date"], "%Y-%m-%d")
            to_date = datetime.datetime.strptime(request.POST["to_date"], "%Y-%m-%d")

        if from_date == None:
            return HttpResponse("error", status=HttpResponse500)

        # ---------- get voice-mail agent list ---------- #
        v_m_agent_list = []
        agent_id_list = list(map(int, user_obj.agents.split(",")))
        for ag_id in agent_id_list:
            agent_dict = atsd_user.getAgentById(ag_id)
            if agent_dict == None:
                continue
            if agent_dict["type"] == 3:
                v_m_agent_list.append(agent_dict)

        # ---------- get voice-mail, average response time chart data ---------- #
        data_vm_chart, data_art_chart = atsd_report.getvmAndArtChartData(email, v_m_agent_list, from_date, to_date, period_id)
        if data_vm_chart == None or data_art_chart == None:
            return HttpResponse("error", status=HttpResponse500)

        data = {
            "v_m_agent_list": v_m_agent_list,
            "data_vm_chart": data_vm_chart,
            "data_art_chart": data_art_chart
        }

        return HttpResponse(json.dumps(data))

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Get Report4 Data
# -----------------------------------------------------------------------------------
@login_required
def getReport4Data(request):
    print("hello")
    try:
        
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(email=email)
        from_date = request.POST["from_date"]
        to_date = request.POST["to_date"]
        message = request.POST["message"]
        status = int(request.POST["status"])
        if status == 0:
            status = None
        type = int(request.POST["type"])
        if type == 0:
            type = None
        call_list = atsd_report.getVoiceMailList(email, from_date, to_date, message, status, type)
        cur_gmtime = time.gmtime()
        cur_time = datetime.datetime(cur_gmtime.tm_year, cur_gmtime.tm_mon, cur_gmtime.tm_mday,
                                     cur_gmtime.tm_hour, cur_gmtime.tm_min, cur_gmtime.tm_sec)
        for call in call_list:
            call_time = datetime.datetime.strptime(call["time"], "%Y-%m-%d %H:%M:%S")
            delta_time = cur_time - call_time
            delta_time_sec = delta_time.days * 86400 + delta_time.seconds
            call["time_since_reception"] = str(math.ceil(delta_time_sec / 60)) + "min"
            advisor = atsd_basic.getAdvisorByPhoneNumber(call["advisor_phone"])
            call["advisor_name"] = ""
            if advisor == None:
                continue

            call["advisor_name"] = advisor["name"]
           # if call["status"] != 3 and delta_time_sec > float(advisor["alert_threshold"]) * 60:
            if call["status"] != 3:
                call["timed_out"] = 1

        total_call = len(call_list)
        total_page = math.ceil(total_call / 15)
        data = {
            "call_list": call_list,
            "total_call": total_call,
            "total_page": total_page
        }
        return HttpResponse(json.dumps(data))
    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: VoiceMail Response View
# -----------------------------------------------------------------------------------
@csrf_exempt
def voiceMailResponse(request, vm_id, replier_id, template_name="userpanel/voicemail_response.html"):
    try:
        vm_obj = tbl_voicemail.objects.get(id=vm_id)
        replier_name = ""

        status = 0
        if vm_obj.status < 2:
            vm_obj.status = 2
            vm_obj.replier_id = replier_id
            vm_obj.save()
            status = 1
        else:
            status = vm_obj.status
            replier_name = atsd_basic.getReplierNameById(vm_id, vm_obj.replier_id)
            if replier_name == None:
                raise Exception()

        data = {
            "vm_id": vm_id,
            "replier_id": replier_id,
            "replier_name": replier_name,
            "status": status,
            "ok_text": vm_obj.ok_text
        }
        return render(request, template_name, data)

    except Exception as e:
        data = {
            "error": 1
        }
        return render(request, template_name, data)


# ***********************************************************************************
# @Function: Send VoiceMail Response
# -----------------------------------------------------------------------------------
@csrf_exempt
def sendVmResponse(request):
    try:
        vm_id = int(request.POST["vm_id"])
        replier_id = int(request.POST["replier_id"])
        sms_response = request.POST["sms_response"]
        replier_name = atsd_basic.getReplierNameById(vm_id, replier_id)
        if replier_name == None:
            raise Exception()

        vm_obj = tbl_voicemail.objects.get(id=vm_id)
        if vm_obj.status == 3:
            return HttpResponse("closed", status=HttpResponse500)

        advisor = atsd_basic.getAdvisorByPhoneNumber(vm_obj.advisor_phone)
        company = atsd_basic.getCompanyById(advisor["company_id"])
        ret_code = glb_twilio.sendSms(company["twilio_account_sid"],
                                      company["twilio_auth_token"],
                                      company["twilio_phone_number"],
                                      vm_obj.caller_phone,
                                      sms_response)
        if ret_code == False:
            return HttpResponse("error", status=HttpResponse500)

        vm_obj.status = 3
        vm_obj.save()

        vm_reply_response_obj = tbl_voicemail_response()
        vm_reply_response_obj.vm_id = vm_id
        vm_reply_response_obj.replier_name = replier_name
        vm_reply_response_obj.message = sms_response
        vm_reply_response_obj.time = datetime.datetime.now()
        vm_reply_response_obj.save()

        return HttpResponse("success")

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Submit Report Of Call
# -----------------------------------------------------------------------------------
@csrf_exempt
def submitReport(request):
    try:
        vm_id = int(request.POST["vm_id"])
        replier_id = int(request.POST["replier_id"])
        report = request.POST["report"]
        replier_name = atsd_basic.getReplierNameById(vm_id, replier_id)
        if replier_name == None:
            raise Exception()

        vm_obj = tbl_voicemail.objects.get(id=vm_id)
        if vm_obj.status == 3:
            return HttpResponse("closed", status=HttpResponse500)

        vm_obj.status = 3
        vm_obj.save()

        vm_reply_response_obj = tbl_voicemail_response()
        vm_reply_response_obj.vm_id = vm_id
        vm_reply_response_obj.replier_name = replier_name
        vm_reply_response_obj.message = report
        vm_reply_response_obj.time = datetime.datetime.now()
        vm_reply_response_obj.save()

        return HttpResponse("success")

    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Dismiss VoiceMail
# -----------------------------------------------------------------------------------
def dismissVoiceMail(request):
    try:
        id = int(request.POST["id"])
        vm_obj = tbl_voicemail.objects.get(id=id)
        vm_obj.status = 3
        vm_obj.save()
        return HttpResponse("success")
    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)


# ***********************************************************************************
# @Function: Flag VoiceMail
# -----------------------------------------------------------------------------------
def flagVoiceMail(request):
    try:
        id = int(request.POST["id"])
        vm_obj = tbl_voicemail.objects.get(id=id)
        vm_obj.flag = 1 - vm_obj.flag
        vm_obj.save()
        return HttpResponse("success")
    except Exception as e:
        return HttpResponse("error", status=HttpResponse500)
