# Generated by Django 2.2.2 on 2019-07-24 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_auto_20190724_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='folder',
        ),
    ]
