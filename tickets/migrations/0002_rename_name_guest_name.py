# Generated by Django 4.2.2 on 2023-06-13 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guest',
            old_name='NAME',
            new_name='Name',
        ),
    ]
