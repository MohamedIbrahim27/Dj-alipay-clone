# Generated by Django 5.0 on 2024-01-13 21:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_token'),
        ('payment', '0005_wallet_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pay',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_payments', to='accounts.profile'),
        ),
        migrations.AlterField(
            model_name='pay',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_payments', to='accounts.profile'),
        ),
    ]
