# Generated by Django 3.2.3 on 2021-06-03 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0008_pic_main'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='photographer',
            options={'ordering': ['display_idx'], 'verbose_name': 'Photographer', 'verbose_name_plural': 'Photographers'},
        ),
        migrations.AlterModelOptions(
            name='pic',
            options={'ordering': ['display_idx'], 'verbose_name': 'Foto', 'verbose_name_plural': 'Fotos'},
        ),
        migrations.RenameField(
            model_name='photographer',
            old_name='display_order',
            new_name='display_idx',
        ),
        migrations.RenameField(
            model_name='pic',
            old_name='display_order',
            new_name='display_idx',
        ),
    ]
