# Generated by Django 4.2.4 on 2023-08-25 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0003_user_foodchoice'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='checkin',
            options={'permissions': [('can_check_in', 'Can allow users to check in'), ('can_view_stats', 'Can view check-in statistics and data'), ('can_manage_all', 'Can manage all operations')]},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('can_check_in', 'Can allow users to check in'), ('can_view_stats', 'Can view check-in statistics and data'), ('can_manage_all', 'Can manage all operations')]},
        ),
    ]
