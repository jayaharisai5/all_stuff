# Generated by Django 4.1.3 on 2022-11-05 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='mlangles_user_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('fname', models.CharField(max_length=100)),
                ('lname', models.CharField(max_length=100)),
                ('org', models.CharField(max_length=100)),
                ('org_mail', models.CharField(max_length=100)),
                ('mobile', models.CharField(max_length=100)),
                ('pass_one', models.CharField(max_length=100)),
            ],
        ),
    ]
