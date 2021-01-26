# Generated by Django 3.1 on 2021-01-26 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_order_used_coupon'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='deliver_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]