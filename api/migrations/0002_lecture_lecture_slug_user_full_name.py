# Generated by Django 5.0 on 2024-01-07 15:12

import autoslug.fields
from django.db import migrations, models
from django.utils.text import slugify

DEFAULT = "abc"

def forwards(apps, _):
    Lecture = apps.get_model("api", "Lecture")
    lectures = Lecture.objects.all()
    for lecture in lectures:
        lecture.lecture_slug = slugify(lecture.lecture_title)
        lecture.save()

    User = apps.get_model("api", "User")
    users = User.objects.all()
    for user in users:
        user.full_name = user.first_name + " " + user.last_name
        user.save()

def backwards(apps, _):
    Lecture = apps.get_model("api", "Lecture")
    lectures = Lecture.objects.all()
    for lecture in lectures:
        lecture.lecture_slug = DEFAULT
        lecture.save()

    User = apps.get_model("api", "User")
    users = User.objects.all()
    for user in users:
        user.full_name = DEFAULT
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='lecture_slug',
            field=autoslug.fields.AutoSlugField(default=DEFAULT, editable=False, populate_from='lecture_title'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='full_name',
            field=models.CharField(default=DEFAULT, max_length=40),
            preserve_default=False,
        ),
        migrations.RunPython(forwards, backwards),
    ]
