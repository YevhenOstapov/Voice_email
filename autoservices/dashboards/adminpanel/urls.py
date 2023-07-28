from django.urls import path, re_path

from . import views

urlpatterns = [
    path("", views.indexView, name="indexView"),
    path("get_page_users", views.getPageUsers, name="getPageUsers"),
    path("register_user", views.registerUser, name="registerUser"),
    path("update_user", views.updateUser, name="updateUser"),
    path("delete_user", views.deleteUser, name="deleteUser"),

    path("agent", views.agentView, name="agentView"),
    path("get_page_agents", views.getPageAgents, name="getPageAgents"),
    path("register_agent", views.registerAgent, name="registerAgent"),
    path("update_agent", views.updateAgent, name="updateAgent"),
    path("delete_agent", views.deleteAgent, name="deleteAgent"),

    path("company", views.companyView, name="companyView"),
    path("get_page_company", views.getPageCompany, name="getPageCompany"),
    path("register_company", views.registerCompany, name="registerCompany"),
    path("update_company", views.updateCompany, name="updateCompany"),
    path("delete_company", views.deleteCompany, name="deleteCompany"),

    path("advisor", views.advisorView, name="advisorView"),
    path("get_page_advisor", views.getPageAdvisor, name="getPageAdvisor"),
    path("register_advisor", views.registerAdvisor, name="registerAdvisor"),
    path("update_advisor", views.updateAdvisor, name="updateAdvisor"),
    path("delete_advisor", views.deleteAdvisor, name="deleteAdvisor"),
]