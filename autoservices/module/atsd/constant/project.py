# ***********************************************************************************
# File Name: project.py
# Author: Dimitar
# Created: 2020-02-22
# Description: Project Constants For AutoserviceDashboard
# -----------------------------------------------------------------------------------

AGENT_TYPE = ["Inbound", "Marketing", "Voicemail"]
PERIOD_TYPE = ["Today", "Yesterday", "Last Week", "Last Month", "From/To"]

API_BASIC_URL = "https://logevent-7ec62.web.app/api/"

API_DASHBOARD_URL = "http://localhost:8300/"

mongo_count_url = "https://us-east-1.aws.webhooks.mongodb-realm.com/api/client/v2.0/app/application-0-qsljw/service/count-event-data/incoming_webhook/count-event-data"
mongo_getdata_url = "https://us-east-1.aws.webhooks.mongodb-realm.com/api/client/v2.0/app/application-0-qsljw/service/getEventdata/incoming_webhook/webhook0"