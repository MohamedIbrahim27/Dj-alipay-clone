# Generated by Django 4.2 on 2023-06-11 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_normaluser_adminuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminuser',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='normaluser',
            name='is_superuser',
            field=models.BooleanField(default=False),
        ),
    ]