# Generated by Django 2.1.2 on 2018-10-17 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0003_book_popularity'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title']},
        ),
    ]
