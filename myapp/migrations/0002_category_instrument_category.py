# Generated by Django 5.1.3 on 2024-11-20 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('instrument', models.CharField(max_length=50)),
                ('type', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='instrument',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instruments', to='myapp.category'),
        ),
    ]
