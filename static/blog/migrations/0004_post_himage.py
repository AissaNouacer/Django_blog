# Generated by Django 3.0.4 on 2020-06-21 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='himage',
            field=models.ImageField(default='default.png', upload_to=''),
        ),
    ]