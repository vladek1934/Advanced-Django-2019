# Generated by Django 2.2.5 on 2019-09-24 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.FileField(default='Images/Default.png', upload_to=''),
        ),
    ]
