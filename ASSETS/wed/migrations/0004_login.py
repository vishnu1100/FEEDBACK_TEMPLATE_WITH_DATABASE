# Generated by Django 3.2.9 on 2023-09-07 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wed', '0003_feedback_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='login',
            fields=[
                ('logid', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=100, verbose_name='username')),
                ('password', models.CharField(max_length=100, verbose_name='password')),
                ('role', models.CharField(max_length=10, verbose_name='role')),
            ],
        ),
    ]
