# Generated by Django 3.1 on 2021-01-13 03:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210113_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='date_create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo'),
        ),
        migrations.AlterField(
            model_name='product',
            name='date_update',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Ngày sửa'),
        ),
    ]