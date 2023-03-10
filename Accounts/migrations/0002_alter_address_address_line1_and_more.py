# Generated by Django 4.0.4 on 2022-11-11 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='Address_line1',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='Address_line2',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='City',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='FullName',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='Landmark',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='MobileNo',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='PinCode',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='login',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='loginprofile',
            name='AlternateMobile',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='loginprofile',
            name='Gender',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='usertype',
            name='LoginTypeName',
            field=models.CharField(max_length=200),
        ),
    ]
