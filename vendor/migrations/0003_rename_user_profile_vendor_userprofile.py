# Generated by Django 4.2.1 on 2023-05-26 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_rename_restaurant_name_vendor_vendor_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vendor',
            old_name='user_profile',
            new_name='userprofile',
        ),
    ]
