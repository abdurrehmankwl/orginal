# Generated by Django 5.1.6 on 2025-05-07 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='llm',
            name='answer',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='llm',
            name='qusetion',
            field=models.TextField(default=''),
        ),
    ]
