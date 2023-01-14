# Generated by Django 3.2 on 2023-01-13 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0002_portfolio_custom_attrs'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='custom_attrs',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='currency',
            name='custom_attrs',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='instrument',
            name='custom_attrs',
            field=models.JSONField(null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='custom_attrs',
            field=models.JSONField(null=True),
        ),
    ]