# Generated by Django 4.2 on 2023-11-24 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_alter_account_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="record", name="money", field=models.FloatField(),
        ),
    ]