# Generated by Django 5.1.4 on 2025-01-05 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_post_highlight_summary_post_list_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='destaque',
            field=models.BooleanField(default=False),
        ),
    ]
