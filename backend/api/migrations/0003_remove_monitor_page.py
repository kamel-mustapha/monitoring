# Generated by Django 4.1 on 2022-12-01 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_monitor_interval_alter_monitor_success_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monitor',
            name='page',
        ),
    ]