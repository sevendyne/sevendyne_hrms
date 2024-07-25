from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0005_alter_attendanceregister_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="gender",
            field=models.CharField(
                blank=True,
                choices=[("Other", "Other"), ("Male", "Male"), ("Female", "Female")],
                max_length=125,
                null=True,
                verbose_name="Gender",
            ),
        ),
    ]
