from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required

from autoservices.database.models import *
from autoservices.module.atsd.constant.ret_code import *
from autoservices.module.atsd import basic as atsd_basic
from autoservices.module.atsd import auth as atsd_auth

# ***********************************************************************************
# @Function: Index View
# -----------------------------------------------------------------------------------
@login_required
def indexView(request):
    try:
        email = request.session.get("email")
        user_obj = tbl_user.objects.get(username=email)
        if user_obj.is_superuser == 1:
            return redirect("/admin")
        else:
            return redirect("/user")
    except Exception as e:
        return redirect("/")


# ***********************************************************************************
# @Function: Account View
# -----------------------------------------------------------------------------------
def accountView(request, user_uid, template_name="home/account.html"):
    try:
        if request.user.is_authenticated:
            return redirect("/")

        alert_str = ""
        key_ary = ["email", "password", "r_password"]
        # ---------- account set case ---------- #
        if atsd_basic.checkKeysInDict(key_ary, request.POST):
            email = request.POST["email"]
            password = request.POST["password"]
            r_password = request.POST["r_password"]
            if password != r_password:
                alert_str = "Password does not match."
            elif len(list(tbl_user.objects.filter(uid=user_uid, email=email))) == 1:
                user_obj = tbl_user.objects.get(uid=user_uid, email=email)
                user_obj.set_password(password)
                user_obj.s_password = password
                user_obj.save()
                ret_code, user_obj = atsd_auth.authenticateUser(email, password)
                django_login(request, user_obj)
                request.session["email"] = email
                request.session.save()
                return redirect("/")
            else:
                alert_str = "Account url or email is invalid."

        data = {
            "user_uid": user_uid,
            "alert_str": alert_str
        }
        return render(request, template_name, data)
    except Exception as e:
        return redirect("/")


# ***********************************************************************************
# @Function: Login
# -----------------------------------------------------------------------------------
def login(request, template_name="home/login.html"):
    try:
        if request.user.is_authenticated:
            return redirect("/")

        key_ary = ["email", "password"]
        alert_str = ""

        # ---------- login case ---------- #
        if atsd_basic.checkKeysInDict(key_ary, request.POST):
            email = request.POST["email"]
            password = request.POST["password"]

            ret_code, user_obj = atsd_auth.authenticateUser(email, password)

            if ret_code == AUTH_SUCCESS:
                django_login(request, user_obj)
                request.session["email"] = email
                request.session.save()
                return redirect("/")

            if ret_code == AUTH_USER_NOT_FOUND or ret_code == AUTH_WRONG_PWD:
                alert_str = "Account is not recognized."
            elif ret_code == AUTH_ACCOUNT_DISABLED:
                alert_str = "Account is disabled."
            elif ret_code == AUTH_UNKOWN_ERROR:
                alert_str = "Sorry, something went wrong."

        data = {
            "alert_str": alert_str
        }
        return render(request, template_name, data)

    except Exception as e:
        return redirect("/")


# ***********************************************************************************
# @Function: Logout
# -----------------------------------------------------------------------------------
@login_required
def logout(request):
    request.session.clear()
    django_logout(request)
    return redirect("/")
