# Generated by Django 4.2.5 on 2023-10-21 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_alter_product_trademark'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtitle',
            name='url',
            field=models.SlugField(default='', max_length=160, verbose_name='URL'),
        ),
    ]