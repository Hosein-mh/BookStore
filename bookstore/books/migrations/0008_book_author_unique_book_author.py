# Generated by Django 3.2 on 2021-04-17 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_auto_20210412_1156'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='book_author',
            constraint=models.UniqueConstraint(fields=('book', 'author'), name='unique_book_author'),
        ),
    ]
