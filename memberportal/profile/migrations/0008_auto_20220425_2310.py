# Generated by Django 3.2.12 on 2022-04-25 13:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0007_auto_20211005_0015"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="member_type",
        ),
        migrations.DeleteModel(
            name="MemberTypes",
        ),
    ]
