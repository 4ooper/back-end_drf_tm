# Generated by Django 4.0.5 on 2022-08-27 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TimeManage', '0017_remove_laboratories_countofready_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratories',
            name='ready',
            field=models.IntegerField(default=2),
        ),
    ]