# Generated by Django 4.1 on 2023-03-04 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_page_html_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpage',
            name='link',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]
