# Sentinel Nexus

Phase 1 foundation for the Sentinel Security & Integrated Facility Management System.

## Included in this checkpoint

- Django project configured for Windows development.
- Environment-based secret and host configuration.
- Secure Django authentication with password hashing.
- Responsive Bootstrap dashboard shell.
- Initial role groups for the planned access-control model.
- SQLite development database, ready to migrate to MySQL or SQL Server later.

Initial role groups: Super Admin, HR Manager, HR Executive, Store Manager,
Storekeeper, Site Supervisor, Operations Manager, Finance Manager, Safety
Officer, Client Manager, Employee and Auditor.

## Run on Windows PowerShell

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py seed_roles
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ and sign in with the superuser account.

## Phase roadmap

1. Foundation, authentication, roles and dashboard
2. Employee master and documents
3. Inventory, stock ledger and employee issue register
4. Attendance, leave, shifts and site operations
5. Procurement, assets, health, safety and reporting

The first business workflow will connect the employee master, inventory stock ledger and uniform issue register so that stock movements remain traceable and cannot be deducted twice.
