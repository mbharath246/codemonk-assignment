# Generated by Django 5.1 on 2024-08-09 02:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_customuser_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='modified_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
