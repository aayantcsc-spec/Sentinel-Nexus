from django.contrib import admin

from .models import (
    Attendance,
    Department,
    Employee,
    EmployeeItemIssue,
    Item,
    ItemCategory,
    ReportSnapshot,
    Site,
    StockTransaction,
    WorkOrder,
)

admin.site.register([Department, Site, Employee, ItemCategory, Item, StockTransaction, EmployeeItemIssue, Attendance, WorkOrder, ReportSnapshot])
