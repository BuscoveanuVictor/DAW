# Generated by Django 5.1.3 on 2024-12-16 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='instrument',
            options={'permissions': [('perm_add_instrument', 'Can add instrument')]},
        ),
    ]
