from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.indexView, name="indexView"),
    path("account/<int:user_uid>", views.accountView, name="accountView"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
]