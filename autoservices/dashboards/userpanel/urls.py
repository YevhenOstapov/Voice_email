from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.indexView, name="indexView"),
    path("report/<int:report_id>", views.reportView, name="reportView"),
    path("get_report1_data", views.getReport1Data, name="getReport1Data"),
    path("get_report2_data", views.getReport2Data, name="getReport2Data"),
    path("get_report3_data", views.getReport3Data, name="getReport3Data"),
    path("get_report4_data", views.getReport4Data, name="getReport4Data"),
    path("voicemail/response/<int:vm_id>/<int:replier_id>", views.voiceMailResponse, name="voiceMailResponse"),
    path("voicemail/send_response", views.sendVmResponse, name="sendVmResponse"),
    path("voicemail/submit_report", views.submitReport, name="submitReport"),
    path("faq", views.faqView, name="faqView"),

    path("voicemail/dismiss_voicemail", views.dismissVoiceMail, name="dismissVoiceMail"),
    path("voicemail/flag_voicemail", views.flagVoiceMail, name="flagVoiceMail"),
]