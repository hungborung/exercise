# Generated by Django 3.1 on 2021-01-26 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20210126_0931'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-create_at',)},
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
