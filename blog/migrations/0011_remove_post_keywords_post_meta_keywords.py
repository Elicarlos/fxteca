# Generated by Django 5.1.4 on 2025-01-12 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_post_meta_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='keywords',
        ),
        migrations.AddField(
            model_name='post',
            name='meta_keywords',
            field=models.CharField(blank=True, help_text='Palavras-chave separadas por vírgulas.', max_length=255, null=True),
        ),
    ]
