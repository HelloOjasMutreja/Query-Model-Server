# Generated by Django 4.1.7 on 2023-04-11 08:00

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('randomizer', '0003_alter_decision_options_decision_is_daily_decision'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
    ]
