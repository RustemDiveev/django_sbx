# Generated by Django 4.0.4 on 2022-06-30 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionTutorialModelDefault',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attr_u', models.CharField(max_length=100, null=True, unique=True)),
                ('attr_nn', models.CharField(max_length=100)),
                ('attr_ut_1', models.CharField(max_length=100, null=True)),
                ('attr_ut_2', models.CharField(max_length=100, null=True)),
            ],
            options={
                'unique_together': {('attr_ut_1', 'attr_ut_2')},
            },
        ),
    ]