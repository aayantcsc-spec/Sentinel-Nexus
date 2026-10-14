from django import forms

from .models import Attendance, Employee, EmployeeItemIssue, Item, Site, WorkOrder


class EmployeeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].initial = "active"
        self.fields["status"].required = False

    class Meta:
        model = Employee
        fields = ["full_name", "phone", "email", "date_of_birth", "joining_date", "department", "designation", "site", "status", "emergency_contact", "address"]
        widgets = {"date_of_birth": forms.DateInput(attrs={"type": "date"}), "joining_date": forms.DateInput(attrs={"type": "date"})}


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name", "category", "sku", "unit", "size", "minimum_stock", "quantity_on_hand"]


class IssueForm(forms.ModelForm):
    class Meta:
        model = EmployeeItemIssue
        fields = ["employee", "item", "quantity", "issue_date", "expected_return_date", "status", "acknowledgement", "notes"]
        widgets = {"issue_date": forms.DateInput(attrs={"type": "date"}), "expected_return_date": forms.DateInput(attrs={"type": "date"})}


class SiteForm(forms.ModelForm):
    class Meta:
        model = Site
        fields = ["name", "client_name", "address", "active"]


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ["employee", "date", "status", "check_in", "check_out", "overtime_hours"]
        widgets = {"date": forms.DateInput(attrs={"type": "date"})}


class WorkOrderForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ["title", "site", "assigned_to", "priority", "status", "due_date", "description"]
        widgets = {"due_date": forms.DateInput(attrs={"type": "date"})}
