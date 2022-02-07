# Generated by Django 3.2.11 on 2022-01-29 14:18

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0010_alter_bookinstance_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('5c363cda-a81a-41d0-9c43-69a727332d35'), help_text='Unique ID for this particular book across the whole library', primary_key=True, serialize=False),
        ),
    ]
