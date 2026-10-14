from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("employees/", views.employees, name="employees"),
    path("employees/add/", views.employee_create, name="employee_create"),
    path("employees/<int:pk>/", views.employee_detail, name="employee_detail"),
    path("inventory/", views.inventory, name="inventory"),
    path("inventory/add/", views.item_create, name="item_create"),
    path("inventory/issues/", views.issue_register, name="issue_register"),
    path("inventory/issues/add/", views.issue_create, name="issue_create"),
    path("operations/", views.operations, name="operations"),
    path("operations/sites/add/", views.site_create, name="site_create"),
    path("operations/attendance/add/", views.attendance_create, name="attendance_create"),
    path("operations/work-orders/add/", views.workorder_create, name="workorder_create"),
    path("reports/", views.reports, name="reports"),
]
