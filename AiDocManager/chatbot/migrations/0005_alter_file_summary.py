# Generated by Django 5.1.6 on 2025-03-01 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbot', '0004_alter_file_document_type_alter_file_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='summary',
            field=models.TextField(blank=True, default='Failed to process', null=True),
        ),
    ]
