# Generated by Django 2.0.1 on 2018-02-15 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20180215_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='user_pic',
            field=models.ImageField(blank=True, default='images/default_user.jpg', null=True, upload_to='images/'),
        ),
    ]
