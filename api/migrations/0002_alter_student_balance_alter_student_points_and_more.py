# Generated by Django 5.0 on 2023-12-16 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='balance',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='student',
            name='points',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='balance',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
