# Generated by Django 4.0.4 on 2022-11-08 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('SupperUserApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BollyWoodCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TagLine', models.TextField(blank=True)),
                ('SubTagLine', models.TextField(blank=True, null=True)),
                ('MainImage', models.ImageField(blank=True, null=True, upload_to='BollywoodMainImage')),
                ('BollyWoodCategorySlug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Homebannerlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BannerTitle', models.CharField(max_length=50)),
                ('BannerDiscount', models.CharField(max_length=20)),
                ('BannerSubtitle', models.CharField(max_length=50)),
                ('BannerBackgroundimg', models.ImageField(blank=True, null=True, upload_to='Homebannerlist')),
                ('Bannersideimg', models.ImageField(blank=True, null=True, upload_to='Homebannerlist')),
            ],
        ),
        migrations.CreateModel(
            name='HomeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HomeCategoryName', models.CharField(max_length=30)),
                ('HomeCategorySlug', models.SlugField(blank=True, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='HomeSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('HomeCategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.homecategory')),
                ('ProductId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SupperUserApp.product')),
            ],
        ),
        migrations.CreateModel(
            name='BollyWoodSubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('BollyWoodCategoryName', models.CharField(blank=True, max_length=50, null=True)),
                ('ProductDetails', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SupperUserApp.product')),
            ],
        ),
    ]
