# Generated by Django 3.1.5 on 2021-03-11 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0004_topic_public'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='topic',
            name='public',
        ),
    ]
