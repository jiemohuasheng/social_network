# Generated by Django 2.0.1 on 2018-02-21 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_user_info_user_pic_crop'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_desc',
            field=models.CharField(blank=True, default=None, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_file',
            field=models.FileField(blank=True, default=None, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='post',
            name='post_title',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='post_user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=None, to='myapp.User_info'),
        ),
    ]
