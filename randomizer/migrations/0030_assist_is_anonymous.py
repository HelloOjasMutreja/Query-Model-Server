# Generated by Django 4.1.7 on 2023-06-14 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('randomizer', '0029_remove_userdecisioninteraction_end_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='assist',
            name='is_anonymous',
            field=models.BooleanField(default=False),
        ),
    ]
