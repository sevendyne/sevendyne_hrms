from datetime import date

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

from apps.employee.models import Department, Designation, Employee
from apps.hrms.models import HrmsClient
from apps.main.functions import get_auto_id
from apps.main.models import Company, CompanyAccess, Country, State


class Command(BaseCommand):
    help = "Seed demo users, company, and sample HRMS data for local development"

    def handle(self, *args, **options):
        self._ensure_groups()
        admin = self._ensure_superuser()
        client_user = self._ensure_hrms_client()
        company = self._ensure_demo_company(admin)
        self._ensure_company_access(client_user, company)
        self._ensure_employee(client_user, company, admin)

        self.stdout.write(self.style.SUCCESS("Demo data seeded successfully."))
        self.stdout.write("")
        self.stdout.write("Login at http://localhost:8000/app/login/")
        self.stdout.write("  Admin:    admin / admin")
        self.stdout.write("  Client:   hrmsclient1 / password@123")
        self.stdout.write("  Employee: employee1 / password@123")

    def _ensure_groups(self):
        groups = [
            ("sevendyne_admin", "can_manage_admin_dashboard"),
            ("hrms_clients", "can_view_hrms_home"),
            ("employee_group", "can_view_employee_dashboard"),
        ]
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType

        content_type = ContentType.objects.get_for_model(Group)
        for group_name, codename in groups:
            group, _ = Group.objects.get_or_create(name=group_name)
            permission, _ = Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={"name": codename.replace("_", " ").title()},
            )
            group.permissions.add(permission)

    def _ensure_superuser(self):
        user, created = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@sevendyne.com",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created or not user.check_password("admin"):
            user.set_password("admin")
            user.is_staff = True
            user.is_superuser = True
            user.save()
        admin_group, _ = Group.objects.get_or_create(name="sevendyne_admin")
        user.groups.add(admin_group)
        return user

    def _ensure_hrms_client(self):
        password = "password@123"
        user, created = User.objects.get_or_create(
            username="hrmsclient1",
            defaults={
                "email": "hrmsclient1@example.com",
                "first_name": "HRMS",
                "last_name": "Client",
                "password": make_password(password),
            },
        )
        if not created:
            user.set_password(password)
            user.save()
        client_group, _ = Group.objects.get_or_create(name="hrms_clients")
        user.groups.add(client_group)
        HrmsClient.objects.update_or_create(
            user=user,
            defaults={
                "first_name": "HRMS",
                "last_name": "Client",
                "email": "hrmsclient1@example.com",
                "username": "hrmsclient1",
                "password": password,
                "is_enabled": True,
                "is_deleted": False,
            },
        )
        return user

    def _ensure_demo_company(self, admin):
        country = Country.objects.first()
        if not country:
            self.stdout.write(
                self.style.WARNING(
                    "No countries loaded. Run: python manage.py loaddata countries states"
                )
            )
            return None
        state = State.objects.filter(country=country).first()
        company, created = Company.objects.get_or_create(
            name="Sevendyne Demo Corp",
            defaults={
                "contact_person": "Demo Admin",
                "address": "123 Demo Street",
                "country": country,
                "state": state,
                "city": "Demo City",
                "postal_code": "10001",
                "email": "demo@sevendyne.com",
                "phone": "+1234567890",
                "auto_id": get_auto_id(Company),
                "creator": admin,
                "updator": admin,
            },
        )
        if created:
            self.stdout.write(f"Created demo company: {company.name}")
        return company

    def _ensure_company_access(self, user, company):
        if not company:
            return
        group, _ = Group.objects.get_or_create(name="hrms_clients")
        CompanyAccess.objects.get_or_create(
            user=user,
            company=company,
            defaults={
                "group": group,
                "is_accepted": True,
                "is_default": True,
            },
        )

    def _ensure_employee(self, creator, company, admin):
        if not company:
            return
        password = "password@123"
        dept, _ = Department.objects.get_or_create(
            company=company,
            name="Engineering",
            defaults={
                "auto_id": get_auto_id(Department),
                "a_id": 1,
                "creator": admin,
                "updator": admin,
            },
        )
        desig, _ = Designation.objects.get_or_create(
            company=company,
            department=dept,
            name="Software Engineer",
            defaults={
                "auto_id": get_auto_id(Designation),
                "a_id": 1,
                "creator": admin,
                "updator": admin,
            },
        )
        user, user_created = User.objects.get_or_create(
            username="employee1",
            defaults={
                "email": "employee1@example.com",
                "first_name": "Demo",
                "last_name": "Employee",
                "password": make_password(password),
            },
        )
        if not user_created:
            user.set_password(password)
            user.save()
        emp_group, _ = Group.objects.get_or_create(name="employee_group")
        user.groups.add(emp_group)
        if not Employee.objects.filter(username="employee1", company=company).exists():
            Employee.objects.create(
                company=company,
                user=user,
                firstname="Demo",
                lastname="Employee",
                username="employee1",
                password=password,
                email="employee1@example.com",
                phone="+1234567890",
                address="456 Employee Ave",
                department=dept,
                designation=desig,
                employeeid="EMP001",
                joindate=date.today(),
                gender="Other",
                auto_id=get_auto_id(Employee),
                a_id=1,
                creator=creator,
                updator=creator,
            )
