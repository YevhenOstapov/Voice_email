from django.urls import path
from . import views

urlpatterns = [
	path('', views.advisor_api, name="advisor-api"),
	path('test-api', views.test_api, name="test_api"),
]