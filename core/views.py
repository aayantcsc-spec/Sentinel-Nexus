from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, F
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AttendanceForm, EmployeeForm, IssueForm, ItemForm, SiteForm, WorkOrderForm
from .models import Attendance, Employee, EmployeeItemIssue, Item, Site, StockTransaction, WorkOrder


def home(request):
    return redirect("dashboard" if request.user.is_authenticated else "login")


@login_required
def dashboard(request):
    context = {
        "metrics": [
            {"label": "Active employees", "value": Employee.objects.filter(status="active").count(), "tone": "blue"},
            {"label": "Present today", "value": Attendance.objects.filter(date=date.today(), status="present").count(), "tone": "green"},
            {"label": "Low-stock items", "value": Item.objects.filter(quantity_on_hand__lte=F("minimum_stock")).count(), "tone": "amber"},
            {"label": "Open work orders", "value": WorkOrder.objects.exclude(status="completed").count(), "tone": "red"},
        ],
        "modules": [
            ("Employees", "Employee master, documents and deployments", "Open module", "employees"),
            ("Inventory", "Uniforms, PPE, stock ledger and issue register", "Open module", "inventory"),
        ],
        "report_cards": [
            ("Employees", Employee.objects.count()),
            ("Inventory items", Item.objects.count()),
            ("Issued items", EmployeeItemIssue.objects.count()),
            ("Work orders", WorkOrder.objects.count()),
        ],
    }
    return render(request, "dashboard.html", context)


@login_required
def employees(request):
    query = request.GET.get("q", "").strip()
    records = Employee.objects.select_related("department", "site").order_by("full_name")
    if query:
        records = records.filter(Q(full_name__icontains=query) | Q(employee_id__icontains=query) | Q(phone__icontains=query))
    return render(request, "module_list.html", {"title": "Employees", "eyebrow": "Phase 2", "records": records, "query": query, "create_url": "employee_create", "columns": ["employee_id", "full_name", "designation", "site", "status"], "empty": "No employees found."})


@login_required
def employee_create(request):
    form = EmployeeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Employee created successfully.")
        return redirect("employees")
    return render(request, "form.html", {"title": "Add employee", "form": form, "back_url": "employees"})


@login_required
def employee_detail(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    return render(request, "employee_detail.html", {"employee": employee, "issues": employee.employeeitemissue_set.select_related("item")})


@login_required
def inventory(request):
    records = Item.objects.select_related("category").order_by("name")
    return render(request, "module_list.html", {"title": "Inventory", "eyebrow": "Phase 3", "records": records, "create_url": "item_create", "columns": ["sku", "name", "category", "size", "quantity_on_hand", "minimum_stock"], "empty": "No inventory items found."})


@login_required
def item_create(request):
    form = ItemForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Inventory item created successfully.")
        return redirect("inventory")
    return render(request, "form.html", {"title": "Add inventory item", "form": form, "back_url": "inventory"})


@login_required
def issue_register(request):
    records = EmployeeItemIssue.objects.select_related("employee", "item").order_by("-issue_date")
    return render(request, "module_list.html", {"title": "Issue register", "eyebrow": "Inventory", "records": records, "create_url": "issue_create", "columns": ["employee", "item", "quantity", "issue_date", "status"], "empty": "No issue transactions found."})


@login_required
def issue_create(request):
    form = IssueForm(request.POST or None)
    if form.is_valid():
        issue = form.save()
        StockTransaction.objects.create(item=issue.item, transaction_type="issue", quantity=issue.quantity, reference=f"Employee issue {issue.employee.employee_id}", created_by=request.user)
        messages.success(request, "Issue transaction recorded.")
        return redirect("issue_register")
    return render(request, "form.html", {"title": "Record employee issue", "form": form, "back_url": "issue_register"})


@login_required
def operations(request):
    orders = WorkOrder.objects.select_related("site", "assigned_to").order_by("-created_at")
    return render(request, "operations.html", {"orders": orders, "sites": Site.objects.order_by("name"), "attendance": Attendance.objects.filter(date=date.today()).select_related("employee")})


@login_required
def site_create(request):
    form = SiteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Site created successfully.")
        return redirect("operations")
    return render(request, "form.html", {"title": "Add site", "form": form, "back_url": "operations"})


@login_required
def attendance_create(request):
    form = AttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Attendance recorded.")
        return redirect("operations")
    return render(request, "form.html", {"title": "Record attendance", "form": form, "back_url": "operations"})


@login_required
def workorder_create(request):
    form = WorkOrderForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Work order created.")
        return redirect("operations")
    return render(request, "form.html", {"title": "Create work order", "form": form, "back_url": "operations"})


@login_required
def reports(request):
    context = {
        "employee_count": Employee.objects.count(),
        "active_count": Employee.objects.filter(status="active").count(),
        "item_count": Item.objects.count(),
        "stock_units": sum(Item.objects.values_list("quantity_on_hand", flat=True)),
        "issue_count": EmployeeItemIssue.objects.count(),
        "work_order_count": WorkOrder.objects.count(),
        "completed_orders": WorkOrder.objects.filter(status="completed").count(),
        "department_counts": Employee.objects.values("department__name").annotate(total=Count("id")).order_by("-total"),
        "report_cards": [
            ("Employees", Employee.objects.count()),
            ("Inventory items", Item.objects.count()),
            ("Issued items", EmployeeItemIssue.objects.count()),
            ("Work orders", WorkOrder.objects.count()),
        ],
    }
    return render(request, "reports.html", context)
