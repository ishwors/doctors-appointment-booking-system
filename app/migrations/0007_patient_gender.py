# Generated by Django 3.2.9 on 2023-07-22 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20230722_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='gender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.gender'),
        ),
    ]
