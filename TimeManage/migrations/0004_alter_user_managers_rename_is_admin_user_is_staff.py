# Generated by Django 4.0.5 on 2022-06-17 09:49

import TimeManage.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TimeManage', '0003_user_alter_relations_userid_delete_profile'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', TimeManage.managers.CustomUserManager()),
            ],
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_admin',
            new_name='is_staff',
        ),
    ]
