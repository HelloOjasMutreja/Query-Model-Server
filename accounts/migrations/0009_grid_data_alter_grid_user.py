# Generated by Django 4.1.7 on 2023-06-15 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_grid'),
    ]

    operations = [
        migrations.AddField(
            model_name='grid',
            name='data',
            field=models.CharField(default='000000000000000000000000000000000000', max_length=36),
        ),
        migrations.AlterField(
            model_name='grid',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
