from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

class Command(BaseCommand):
    help = 'Create user groups and permissions'

    def handle(self, *args, **options):
        # Define group and permission information
        groups_and_permissions = [
            ('sevendyne_admin', 'can_manage_admin_dashboard'),
            ('hrms_clients', 'can_view_hrms_home'),
            ('employee_group', 'can_view_employee_dashboard')
            # Add more groups and permissions as needed
        ]

        for group_name, permission_codename in groups_and_permissions:
            # Get or create the group
            group, created = Group.objects.get_or_create(name=group_name)

            # Get or create the permission
            content_type = ContentType.objects.get_for_model(Group)  # Use Group as an example model
            permission, permission_created = Permission.objects.get_or_create(
                codename=permission_codename,
                content_type=content_type,
            )

            # Add the permission to the group
            group.permissions.add(permission)

            if created or permission_created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created with permission "{permission_codename}"'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" already exists. Permission "{permission_codename}" added.'))

        self.stdout.write(self.style.SUCCESS('Groups and permissions creation complete.'))
