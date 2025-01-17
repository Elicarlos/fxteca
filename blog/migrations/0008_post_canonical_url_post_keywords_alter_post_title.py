# Generated by Django 5.1.4 on 2025-01-05 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_post_destaque'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='canonical_url',
            field=models.URLField(blank=True, help_text='URL canônica para evitar duplicação.', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='keywords',
            field=models.TextField(blank=True, help_text='Palavras-chave separadas por vírgulas.', null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
