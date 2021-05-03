# Generated by Django 3.2 on 2021-05-03 00:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='photographer',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='portfolio.photographer'),
        ),
    ]
