# Generated by Django 5.0.3 on 2025-01-16 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('absent', '0002_alter_absent_response_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='absent',
            options={'ordering': ('-create_time',)},
        ),
    ]
