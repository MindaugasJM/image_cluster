# Generated by Django 4.0.5 on 2022-06-28 12:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Image', 'verbose_name_plural': 'Images'},
        ),
    ]
