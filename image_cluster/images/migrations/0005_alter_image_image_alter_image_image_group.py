# Generated by Django 4.0.5 on 2022-06-29 15:49

from django.db import migrations, models
import images.models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0004_remove_image_image_features_alter_image_image_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=images.models.image_path_n_file_name, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_group',
            field=models.IntegerField(null=True, verbose_name='image group'),
        ),
    ]
