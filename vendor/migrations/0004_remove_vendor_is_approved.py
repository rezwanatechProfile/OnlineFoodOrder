# Generated by Django 4.2.1 on 2023-05-28 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0003_rename_user_profile_vendor_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='is_approved',
        ),
    ]
