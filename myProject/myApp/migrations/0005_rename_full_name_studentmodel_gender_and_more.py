# Generated by Django 4.2.6 on 2023-10-14 04:14

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0004_studentmodel"),
    ]

    operations = [
        migrations.RenameField(
            model_name="studentmodel",
            old_name="full_name",
            new_name="gender",
        ),
        migrations.AddField(
            model_name="studentmodel",
            name="courseid",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="myApp.coursemodel",
            ),
        ),
        migrations.AddField(
            model_name="studentmodel",
            name="cratedat",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name="studentmodel",
            name="sessionyearid",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="myApp.sessionyear",
            ),
        ),
        migrations.AddField(
            model_name="studentmodel",
            name="updateat",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="studentmodel",
            name="student_id",
            field=models.IntegerField(),
        ),
    ]
