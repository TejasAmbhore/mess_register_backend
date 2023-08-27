# Generated by Django 4.2.4 on 2023-08-27 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkin', '0004_alter_checkin_options_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkin',
            name='food_type',
            field=models.CharField(choices=[('veg', 'Veg'), ('nonveg', 'Non-Veg')], default='veg', max_length=10),
        ),
    ]
