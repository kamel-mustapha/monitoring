# Generated by Django 4.1 on 2023-03-29 22:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_eventstats'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventstats',
            name='date',
            field=models.DateField(),
        ),
    ]
