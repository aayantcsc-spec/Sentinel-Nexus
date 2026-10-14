from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


ROLE_NAMES = [
    "Super Admin",
    "HR Manager",
    "HR Executive",
    "Store Manager",
    "Storekeeper",
    "Site Supervisor",
    "Operations Manager",
    "Finance Manager",
    "Safety Officer",
    "Client Manager",
    "Employee",
    "Auditor",
]


class Command(BaseCommand):
    help = "Create the initial Sentinel Nexus role groups."

    def handle(self, *args, **options):
        created = 0
        for role_name in ROLE_NAMES:
            _, was_created = Group.objects.get_or_create(name=role_name)
            created += int(was_created)
        self.stdout.write(self.style.SUCCESS(f"Roles ready. Created {created} new role(s)."))

