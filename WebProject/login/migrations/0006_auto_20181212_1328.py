# Generated by Django 2.1.2 on 2018-12-12 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_auto_20181212_1324'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userlike',
            old_name='following',
            new_name='liked',
        ),
    ]