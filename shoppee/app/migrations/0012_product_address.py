# Generated by Django 5.0.4 on 2024-05-14 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_product_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
