# Generated by Django 3.2.9 on 2023-06-25 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_patient_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='profile_pic',
            field=models.ImageField(blank=True, default='default.png', null=True, upload_to=''),
        ),
    ]
