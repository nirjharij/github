# Generated by Django 2.1 on 2018-08-12 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapi', '0003_auto_20180812_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpublicrepodata',
            name='description',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
