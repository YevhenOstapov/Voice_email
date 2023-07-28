from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer
from autoservices import settings
from autoservices.database.models import tb_Category_Model,tbl_advisor
import json
from django.db import connection
from django.http import HttpResponse
import requests


@api_view(['POST'])
def advisor_api(request):
    try:
        phone_number = request.data['phone_number']
    except Exception as e:
        return Response({'status': 'Fail','message': 'phone-number is required'})
    try:
           #phone_number = request.data['phone_number']
           advisor = tbl_advisor.objects.get(phone_number=phone_number)
    except tbl_advisor.DoesNotExist:
           return Response({'status': 'Fail','message': 'phone-number doesnot exsist'})
    try:
        name = 'database_tbl_advisor'
        api_key = request.data['api_key']
        if api_key != settings.API_KEY:
            return Response({'status': 'Fail','message': 'Api key does not exist'})
        try:
            table = tb_Category_Model.objects.get(name=name)
            cursor = connection.cursor()
            value = table.value.strip("{}", )
            #cursorQuery = "SELECT " + value + " FROM " + name + ""
            #cursorQuery="SELECT " + value + " FROM " + name + " WHERE database_tbl_advisor.company_id = database_tbl_company.id"
            cursorQuery="SELECT " + value + " FROM database_tbl_advisor LEFT JOIN database_tbl_company ON database_tbl_advisor.company_id=database_tbl_company.id WHERE phone_number = " + advisor.phone_number + ""
            cursor.execute(cursorQuery)
            records = cursor.fetchall()
            insertObject = []
            columnNames = [column[0] for column in cursor.description]
            for record in records:
                insertObject.append(dict(zip(columnNames, record)))
                row = insertObject
            if len(row) != 0:
                return Response({'status': 'Success', 'data': row})
            else:
                return Response({'status': 'Fail', 'message': 'Data not found.'})
        except tb_Category_Model.DoesNotExist:
            return Response({'status': 'Fail','message': 'tabel Data not found.'})
    except Exception as e:
       print(e)
       return Response({'status': 'Fail','message': 'api_key is required'})


def test_api(request):
    url="https://us-east-1.aws.webhooks.mongodb-realm.com/api/client/v2.0/app/application-0-qsljw/service/createEventInSql/incoming_webhook/logevent?secret=123123&agent=testagent2"
    res = requests.get(url)
    return HttpResponse(res)
         
