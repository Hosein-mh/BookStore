# Generated by Django 3.2 on 2021-04-11 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20210410_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='books', to='books.Tag'),
        ),
    ]
