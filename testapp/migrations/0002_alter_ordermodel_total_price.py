# Generated by Django 5.1.5 on 2025-02-11 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
