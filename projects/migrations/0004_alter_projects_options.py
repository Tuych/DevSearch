# Generated by Django 5.0.1 on 2024-09-15 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_alter_projects_options_review'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projects',
            options={'ordering': ['-vote_ratio', '-vote_total', 'title']},
        ),
    ]
