# Generated by Django 5.0.1 on 2024-02-03 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_language_alpha2_language_alpha3t'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='data',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
