# Generated by Django 3.1 on 2021-01-28 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_product_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='num_available',
            field=models.IntegerField(default=1),
        ),
    ]
