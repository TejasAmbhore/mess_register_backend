# Generated by Django 4.2.4 on 2023-09-12 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0007_user_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
