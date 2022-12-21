# Generated by Django 4.0.4 on 2022-11-08 10:43

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Accounts', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AddToCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateTime', models.DateTimeField(auto_now_add=True)),
                ('Qunatity', models.IntegerField()),
                ('TotalPrice', models.FloatField()),
                ('MoneyStatus', models.BooleanField(default=0)),
                ('orderid', models.CharField(blank=True, max_length=100, null=True)),
                ('razor_pay_order_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razor_pay_payment_id', models.CharField(blank=True, max_length=100, null=True)),
                ('razor_pay_payment_signature', models.CharField(blank=True, max_length=100, null=True)),
                ('OrderDate', models.DateField(blank=True, null=True)),
                ('CancelledStatus', models.BooleanField(blank=True, default=0, null=True)),
                ('CancelDate', models.DateField(blank=True, null=True)),
                ('DeliveryStatus', models.BooleanField(blank=True, default=0, null=True)),
                ('DeliveryDate', models.DateField(blank=True, null=True)),
                ('ExtimateDeliveryAddress', models.DateField(blank=True, null=True)),
                ('RefundStatus', models.BooleanField(blank=True, default=0, null=True)),
                ('RefundDate', models.DateField(blank=True, null=True)),
                ('Exchangedate', models.DateField(blank=True, null=True)),
                ('ExchangeStatus', models.BooleanField(blank=True, default=0, null=True)),
                ('ReturnrequestbyDate', models.DateField(blank=True, null=True)),
                ('ReturnRequest', models.BooleanField(blank=True, default=0, null=True)),
                ('ReturnrequestDate', models.DateField(blank=True, null=True)),
                ('ReturnRequestStatus', models.BooleanField(blank=True, default=0, null=True)),
                ('Payment_method', models.CharField(blank=True, max_length=50, null=True)),
                ('LoginId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryLevel1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CategoryName', models.CharField(max_length=20)),
                ('CategoryImage', models.ImageField(upload_to='CategoryLevel1')),
                ('CategoryDescription', models.TextField(blank=True, null=True)),
                ('CategorySlug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('SubCategoryName', models.JSONField(blank=True, null=True)),
                ('CategoryProductCount', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryLevel2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CategoryLevel2Name', models.CharField(blank=True, max_length=30, null=True)),
                ('CategoryImages', models.ImageField(blank=True, default='', null=True, upload_to='CategoryLevel2')),
                ('CategoryDescription', models.TextField(blank=True, null=True)),
                ('CategorySlug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('CategoryLevel1Id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SupperUserApp.categorylevel1')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryLevel3',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CategoryLevel3Name', models.CharField(max_length=30)),
                ('CategoryImages', models.ImageField(blank=True, default='', null=True, upload_to='CategoryLevel2')),
                ('CategoryDescription', models.TextField(blank=True, null=True)),
                ('CategorySlug', models.SlugField(max_length=200, unique=True)),
                ('productcount', models.IntegerField(blank=True, default=0, null=True)),
                ('CategoryLevel2Id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SupperUserApp.categorylevel2')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductName', models.CharField(max_length=30)),
                ('ProductDescription', models.TextField(blank=True, null=True)),
                ('Star', models.FloatField(blank=True, default=0, null=True)),
                ('TotalRatingCount', models.IntegerField(blank=True, default=0, null=True)),
                ('TotalReviewCount', models.IntegerField(blank=True, default=0, null=True)),
                ('ProductSlug', models.SlugField(blank=True, max_length=200, null=True, unique=True)),
                ('ProductMainImage', models.ImageField(blank=True, null=True, unique=True, upload_to='ProductmainImage')),
                ('ProductBrandName', models.CharField(blank=True, max_length=50, null=True)),
                ('file1', models.ImageField(blank=True, null=True, upload_to='file1')),
                ('file2', models.ImageField(blank=True, null=True, upload_to='file2')),
                ('file3', models.ImageField(blank=True, null=True, upload_to='file3')),
                ('file4', models.ImageField(blank=True, null=True, upload_to='file4')),
                ('file5', models.ImageField(blank=True, null=True, upload_to='file5')),
                ('file6', models.FileField(blank=True, null=True, upload_to='file6')),
                ('TotalProduct', models.IntegerField(blank=True, null=True)),
                ('Price', models.FloatField(blank=True, null=True)),
                ('DiscountPercent', models.FloatField(blank=True, default=0, null=True)),
                ('Product_Specification', ckeditor.fields.RichTextField(blank=True, default=0, null=True)),
                ('CategoryLevel1Id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SupperUserApp.categorylevel1')),
                ('CategoryLevel2Id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SupperUserApp.categorylevel2')),
                ('CategoryLevel3Id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SupperUserApp.categorylevel3')),
            ],
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductColorName', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Review_products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Review', models.TextField(blank=True, null=True)),
                ('Review_Date', models.DateField()),
                ('Image1', models.FileField(blank=True, null=True, upload_to='ReviewImage1')),
                ('Image2', models.FileField(blank=True, null=True, upload_to='ReviewImage2')),
                ('Cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SupperUserApp.product')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='Review_dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='Review_likes', to=settings.AUTH_USER_MODEL)),
                ('login_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Return_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Reason', models.CharField(blank=True, max_length=100, null=True)),
                ('Message', models.TextField(blank=True, null=True)),
                ('Date', models.DateField()),
                ('Accept_decline', models.IntegerField(blank=True, null=True)),
                ('submit', models.BooleanField(default=False)),
                ('submit_date', models.DateField(blank=True, null=True)),
                ('submitMessage', models.TextField(blank=True, null=True)),
                ('ProductId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SupperUserApp.addtocart')),
                ('login', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rating_Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Rating_star', models.IntegerField(default=0, validators=[django.core.validators.MaxLengthValidator(5), django.core.validators.MinLengthValidator(0)])),
                ('Cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SupperUserApp.product')),
                ('login_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionsAndAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Question', models.TextField()),
                ('Answer', models.TextField()),
                ('Date', models.DateField(auto_now_add=True)),
                ('Addedby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ProductId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='SupperUserApp.product')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productDetail', models.JSONField(blank=True)),
                ('Product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SupperUserApp.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSizeColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductImage', models.ImageField(blank=True, null=True, upload_to='ProductColourImage')),
                ('Stock', models.IntegerField()),
                ('Price', models.FloatField(blank=True, null=True)),
                ('DiscountPercent', models.FloatField(blank=True, default=0, null=True)),
                ('Product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SupperUserApp.product')),
                ('ProductColour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SupperUserApp.productcolor')),
                ('ProductSize', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='SupperUserApp.productsize')),
            ],
        ),
        migrations.CreateModel(
            name='ProductColourImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ProductImageName', models.CharField(max_length=50, null=True)),
                ('ProductColourImage', models.ImageField(blank=True, null=True, upload_to='ProductColourImage')),
                ('ProductColor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='SupperUserApp.productcolor')),
            ],
        ),
        migrations.AddField(
            model_name='addtocart',
            name='ProductSizeColorId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SupperUserApp.productsizecolor'),
        ),
        migrations.AddField(
            model_name='addtocart',
            name='delivry_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Accounts.address'),
        ),
    ]
