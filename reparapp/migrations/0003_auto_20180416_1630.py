# Generated by Django 2.0.4 on 2018-04-16 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reparapp', '0002_auto_20180416_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reparacion',
            name='fecha_salida',
            field=models.DateField(blank=True, null=True),
        ),
    ]