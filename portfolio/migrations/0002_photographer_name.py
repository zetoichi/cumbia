# Generated by Django 3.2 on 2021-05-02 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='photographer',
            name='name',
            field=models.CharField(default='', max_length=250),
        ),
    ]
