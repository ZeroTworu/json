# Generated by Django 5.1.2 on 2024-10-10 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_basicuser_step3'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basicuser',
            name='step3',
        ),
    ]
