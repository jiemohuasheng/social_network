# Generated by Django 2.0.1 on 2018-02-15 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_user_info_user_web_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='user_web_url',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
