# Generated by Django 2.1 on 2018-09-06 02:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20180831_1605'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name_plural': 'questions'},
        ),
        migrations.AlterModelTable(
            name='question',
            table='questions',
        ),
    ]
