# Generated by Django 3.2.9 on 2023-06-28 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_auto_20230628_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Specialization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='doctor',
            name='gender',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.gender'),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='specialization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.specialization'),
        ),
    ]