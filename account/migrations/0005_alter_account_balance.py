# Generated by Django 4.2 on 2023-11-24 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0004_alter_cookie_live"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account", name="balance", field=models.FloatField(),
        ),
    ]
