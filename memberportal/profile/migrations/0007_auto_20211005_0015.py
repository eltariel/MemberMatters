# Generated by Django 3.2.2 on 2021-10-04 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profile", "0006_auto_20210427_1500"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="groups",
        ),
        migrations.AlterField(
            model_name="log",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="membertypes",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="profile",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
