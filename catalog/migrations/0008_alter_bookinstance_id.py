# Generated by Django 3.2.11 on 2022-01-29 06:51

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_auto_20220129_0720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinstance',
            name='id',
            field=models.UUIDField(default=uuid.UUID('dce2b4a1-7543-4b48-a185-dabe5abc3038'), help_text='Unique ID for this particular book across the whole library', primary_key=True, serialize=False),
        ),
    ]
