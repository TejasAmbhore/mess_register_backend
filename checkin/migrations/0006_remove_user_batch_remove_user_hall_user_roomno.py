# Generated by Django 4.2.4 on 2023-09-12 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0005_checkin_food_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='batch',
        ),
        migrations.RemoveField(
            model_name='user',
            name='hall',
        ),
        migrations.AddField(
            model_name='user',
            name='roomNo',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]
