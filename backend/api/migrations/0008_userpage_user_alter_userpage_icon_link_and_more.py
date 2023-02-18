# Generated by Django 4.1 on 2023-02-18 16:07

import api.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0007_alter_userpage_icon_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpage',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userpage',
            name='icon_link',
            field=models.ImageField(blank=True, null=True, upload_to=api.models.UserPage.personal_image_filename),
        ),
        migrations.AlterField(
            model_name='userpage',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.page'),
        ),
    ]
