# Generated by Django 3.2.13 on 2022-11-12 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estacao',
            name='dia',
            field=models.IntegerField(),
        ),
    ]