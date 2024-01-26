# Generated by Django 5.0 on 2023-12-16 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_wallet_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='pay',
            name='status',
            field=models.CharField(choices=[('PAY', 'PAY'), ('RECEIV', 'RECEIV'), ('TRANSFORM', 'TRANSFORM')], default='', max_length=12),
            preserve_default=False,
        ),
    ]
