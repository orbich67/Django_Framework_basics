# Generated by Django 3.2.8 on 2021-11-11 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20211111_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=1, verbose_name='пол'),
        ),
    ]
