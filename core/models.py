from django.conf import settings
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Site(models.Model):
    name = models.CharField(max_length=160)
    client_name = models.CharField(max_length=160, blank=True)
    address = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("leave", "On leave"),
        ("suspended", "Suspended"),
        ("resigned", "Resigned"),
        ("terminated", "Terminated"),
    ]
    employee_id = models.CharField(max_length=30, unique=True, blank=True)
    full_name = models.CharField(max_length=160)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    joining_date = models.DateField()
    department = models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True)
    designation = models.CharField(max_length=120, blank=True)
    site = models.ForeignKey(Site, on_delete=models.PROTECT, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    emergency_contact = models.CharField(max_length=160, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.employee_id:
            latest = Employee.objects.order_by("-id").first()
            self.employee_id = f"EMP-{(latest.id + 1 if latest else 1):04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"


class ItemCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=160)
    category = models.ForeignKey(ItemCategory, on_delete=models.PROTECT)
    sku = models.CharField(max_length=60, unique=True)
    unit = models.CharField(max_length=30, default="piece")
    size = models.CharField(max_length=20, blank=True)
    minimum_stock = models.PositiveIntegerField(default=0)
    quantity_on_hand = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.sku})"


class StockTransaction(models.Model):
    TYPE_CHOICES = [("receipt", "Receipt"), ("issue", "Issue"), ("return", "Return"), ("adjustment", "Adjustment")]
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantity = models.PositiveIntegerField()
    reference = models.CharField(max_length=120, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            delta = self.quantity if self.transaction_type in {"receipt", "return"} else -self.quantity
            self.item.quantity_on_hand = models.F("quantity_on_hand") + delta
            self.item.save(update_fields=["quantity_on_hand"])
        super().save(*args, **kwargs)


class EmployeeItemIssue(models.Model):
    STATUS_CHOICES = [("issued", "Issued"), ("returned", "Returned"), ("damaged", "Damaged"), ("lost", "Lost")]
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    issue_date = models.DateField()
    expected_return_date = models.DateField(null=True, blank=True)
    actual_return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="issued")
    acknowledgement = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.employee} - {self.item}"


class Attendance(models.Model):
    STATUS_CHOICES = [("present", "Present"), ("absent", "Absent"), ("leave", "Leave"), ("off", "Weekly off")]
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="present")
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["employee", "date"], name="unique_employee_attendance_day")]


class WorkOrder(models.Model):
    PRIORITY_CHOICES = [("low", "Low"), ("normal", "Normal"), ("high", "High"), ("urgent", "Urgent")]
    STATUS_CHOICES = [("open", "Open"), ("in_progress", "In progress"), ("completed", "Completed")]
    title = models.CharField(max_length=180)
    site = models.ForeignKey(Site, on_delete=models.PROTECT)
    assigned_to = models.ForeignKey(Employee, on_delete=models.PROTECT, null=True, blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default="normal")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")
    due_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ReportSnapshot(models.Model):
    name = models.CharField(max_length=160)
    report_type = models.CharField(max_length=80)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
