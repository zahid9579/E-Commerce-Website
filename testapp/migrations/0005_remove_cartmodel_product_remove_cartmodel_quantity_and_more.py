# Generated by Django 5.1.5 on 2025-02-11 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0004_ordermodel_products'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartmodel',
            name='product',
        ),
        migrations.RemoveField(
            model_name='cartmodel',
            name='quantity',
        ),
        migrations.AddField(
            model_name='cartmodel',
            name='products',
            field=models.ManyToManyField(to='testapp.productmodel'),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
