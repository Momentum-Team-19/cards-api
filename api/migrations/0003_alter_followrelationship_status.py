# Generated by Django 4.2.5 on 2023-09-18 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_card_draft'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followrelationship',
            name='status',
            field=models.IntegerField(choices=[(1, 'Following'), (0, 'Blocked')], default=1),
        ),
    ]
