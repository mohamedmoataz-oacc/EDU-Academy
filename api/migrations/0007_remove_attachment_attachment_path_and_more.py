# Generated by Django 5.0 on 2023-12-17 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_course_thumbnail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='attachment_path',
        ),
        migrations.RemoveField(
            model_name='lecture',
            name='video_path',
        ),
        migrations.AddField(
            model_name='attachment',
            name='attachment',
            field=models.FileField(max_length=250, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='lecture',
            name='video',
            field=models.FileField(max_length=250, null=True, upload_to=''),
        ),
    ]