# Generated by Django 2.0 on 2020-11-27 19:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0009_auto_20201127_1652'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='reply',
            new_name='reply_to',
        ),
    ]
