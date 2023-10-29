# Generated by Django 4.2.6 on 2023-10-22 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0014_staffnotificationmodel_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="teacherLeaveModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("data", models.CharField(max_length=100)),
                ("message", models.TextField()),
                ("status", models.IntegerField(default=0)),
                ("createAt", models.DateTimeField(auto_now_add=True)),
                ("updateat", models.DateTimeField(auto_now_add=True)),
                (
                    "staff_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="myApp.teachermodel",
                    ),
                ),
            ],
        ),
    ]