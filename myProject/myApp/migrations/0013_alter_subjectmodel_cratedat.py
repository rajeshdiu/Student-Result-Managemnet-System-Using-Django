# Generated by Django 4.2.6 on 2023-10-21 12:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myApp", "0012_staffnotificationmodel"),
    ]

    operations = [
        migrations.AlterField(
            model_name="subjectmodel",
            name="cratedat",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
