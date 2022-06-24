# Generated by Django 4.0.4 on 2022-06-24 10:00

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('drf_nested_url', '0002_alter_contact_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=1000, overwrite=True, populate_from='slug_populate_from', unique=True),
        ),
    ]