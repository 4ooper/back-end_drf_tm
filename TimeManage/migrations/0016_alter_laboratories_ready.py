# Generated by Django 4.0.5 on 2022-08-27 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeManage', '0015_alter_laboratories_ready'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laboratories',
            name='ready',
            field=models.JSONField(blank=True, default=[], null=True),
        ),
    ]
