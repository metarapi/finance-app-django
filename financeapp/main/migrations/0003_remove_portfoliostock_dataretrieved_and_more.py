# Generated by Django 5.0.4 on 2024-04-07 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_stock_ticker'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='portfoliostock',
            name='dataRetrieved',
        ),
        migrations.AddField(
            model_name='stock',
            name='dataRetrieved',
            field=models.BooleanField(default=False),
        ),
    ]
