import pytest
from django.contrib.auth.models import Group, User
from django.core.management import call_command

from apps.employee.models import Department, Designation, Employee
from apps.hrms.models import HrmsClient
from apps.main.management.commands.seed_demo_data import Command
from apps.main.models import Company, CompanyAccess, Country, State

"""
Tests for the seed_demo_data management command.
"""


# instance of the Command class
@pytest.fixture
def command():
    return Command()


# seed administrative level groups
@pytest.fixture
def seeded_groups(db, command):
    return command._ensure_groups()


# seed a country and a state. Needed for demo company tests
@pytest.fixture
def country_state(db):
    country = Country.objects.create(
        name="Afghanistan",
        iso3="AFG",
        iso2="AF",
        numeric_code="004",
        phone_code="93",
        capital="Kabul",
        currency="AFN",
        currency_symbol="؋",
        tld=".af",
        native="افغانستان",
        region="Asia",
        subregion="Southern Asia",
        latitude="33.00000000",
        longitude="65.00000000",
    )
    state = State.objects.create(
        name="Ghazni",
        country=country,
        country_code="AF",
        state_code="GHA",
        latitude="33.54505870",
        longitude="68.41739720",
    )
    return country, state


# test admin user
@pytest.mark.django_db
class TestSeedDemoDataEnsureSuperuser:
    def test_admin_user_is_created(self, command, seeded_groups):
        user = command._ensure_superuser()

        assert User.objects.filter(username="admin").exists()
        assert Group.objects.filter(name="sevendyne_admin").exists()

        assert user.groups.filter(name="sevendyne_admin").exists()
        assert user.groups.filter(
            permissions__codename="can_manage_admin_dashboard"
        ).exists()
        assert user.check_password("admin")
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_fixes_password_on_existing_user(self, command, seeded_groups):
        existing = User.objects.create(
            username="admin", is_staff=False, is_superuser=False
        )
        existing.set_password("wrong-password")
        existing.save()

        user = command._ensure_superuser()
        user.refresh_from_db()

        assert user.check_password("admin")
        assert user.is_staff is True
        assert user.is_superuser is True

    def test_idempotent(self, command, seeded_groups):
        command._ensure_superuser()
        command._ensure_superuser()

        assert User.objects.filter(username="admin").count() == 1


# test HRMS client
@pytest.mark.django_db
class TestSeedDemoDaatEnsureHrmsClient:
    def test_hrms_client_user_is_created(self, command, seeded_groups):
        user = command._ensure_hrms_client()

        assert User.objects.filter(username="hrmsclient1").exists()
        assert Group.objects.filter(name="hrms_clients").exists()

        assert user.groups.filter(name="hrms_clients").exists()
        assert user.groups.filter(permissions__codename="can_view_hrms_home").exists()
        assert user.check_password("password@123")

    def test_hrms_client_profile_created(self, command, seeded_groups):
        command._ensure_hrms_client()

        client = HrmsClient.objects.get(username="hrmsclient1")
        assert client.email == "hrmsclient1@example.com"
        assert client.is_enabled is True
        assert client.is_deleted is False

    def test_idempotent(self, command, seeded_groups):
        command._ensure_hrms_client()
        command._ensure_hrms_client()

        assert User.objects.filter(username="hrmsclient1").count() == 1
        assert HrmsClient.objects.filter(username="hrmsclient1").count() == 1


# test demo company
@pytest.mark.django_db
class TestSeedDemoDataEnsureDemoCompany:
    def test_returns_none_when_no_country_exists(self, command, seeded_groups):
        admin = command._ensure_superuser()

        company = command._ensure_demo_company(admin)

        assert company is None
        assert not Company.objects.filter(name="Sevendyne Demo Corp").exists()

    def test_creates_company_when_country_exists(
        self, command, seeded_groups, country_state
    ):
        admin = command._ensure_superuser()

        company = command._ensure_demo_company(admin)

        assert company is not None
        assert company.name == "Sevendyne Demo Corp"


# test employee
@pytest.mark.django_db
class TestSeedDemoDataEnsureEmployee:
    def test_employee_user_created_with_group(
        self, command, seeded_groups, country_state
    ):
        admin = command._ensure_superuser()
        client_user = command._ensure_hrms_client()
        company = command._ensure_demo_company(admin)

        command._ensure_employee(client_user, company, admin)

        user = User.objects.get(username="employee1")
        assert user.check_password("password@123")
        assert Group.objects.filter(name="employee_group").exists()
        assert user.groups.filter(name="employee_group").exists()

    def test_employee_record_created(self, command, seeded_groups, country_state):
        admin = command._ensure_superuser()
        client_user = command._ensure_hrms_client()
        company = command._ensure_demo_company(admin)

        command._ensure_employee(client_user, company, admin)

        employee = Employee.objects.get(username="employee1", company=company)
        assert employee.employeeid == "EMP001"
        assert employee.department.name == "Engineering"
        assert employee.designation.name == "Software Engineer"

    def test_no_operation_when_company_is_none(self, seeded_groups, command):
        admin = command._ensure_superuser()
        client_user = command._ensure_hrms_client()

        command._ensure_employee(client_user, None, admin)

        assert not Employee.objects.filter(username="employee1").exists()

    def test_idempotent(self, command, seeded_groups, country_state):
        admin = command._ensure_superuser()
        client_user = command._ensure_hrms_client()
        company = command._ensure_demo_company(admin)

        command._ensure_employee(client_user, company, admin)
        command._ensure_employee(client_user, company, admin)

        assert (
            Employee.objects.filter(username="employee1", company=company).count() == 1
        )
        assert User.objects.filter(username="employee1").count() == 1


# integration test for the Command class
@pytest.mark.django_db
class TestSeedDemoDataCommand:
    def test_full_command_creates_all_demo_data(self, country_state):
        call_command("seed_demo_data")

        admin = User.objects.get(username="admin")
        assert admin.is_superuser is True

        client = User.objects.get(username="hrmsclient1")
        assert client.groups.filter(name="hrms_clients").exists()

        employee = User.objects.get(username="employee1")
        assert employee.groups.filter(name="employee_group").exists()

        company = Company.objects.get(name="Sevendyne Demo Corp")
        assert CompanyAccess.objects.filter(user=client, company=company).exists()
        assert Employee.objects.filter(username="employee1", company=company).exists()

    def test_full_command_is_idempotent(self, country_state):
        call_command("seed_demo_data")
        call_command("seed_demo_data")

        assert User.objects.filter(username="admin").count() == 1
        assert User.objects.filter(username="hrmsclient1").count() == 1
        assert User.objects.filter(username="employee1").count() == 1
        assert Company.objects.filter(name="Sevendyne Demo Corp").count() == 1
