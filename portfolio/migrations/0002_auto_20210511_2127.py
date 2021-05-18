# Generated by Django 3.2.2 on 2021-05-11 21:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_order', models.IntegerField(verbose_name='Orden')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('photographer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='portfolio.photographer')),
            ],
        ),
        migrations.AlterField(
            model_name='pic',
            name='picset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pics', to='portfolio.portfolio'),
        ),
        migrations.DeleteModel(
            name='PicSet',
        ),
    ]