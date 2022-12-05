# Generated by Django 4.1.3 on 2022-12-05 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name_kr', models.CharField(max_length=50, verbose_name='브랜드명_국문')),
                ('brand_name_en', models.CharField(max_length=50, verbose_name='브랜드명_영문')),
                ('brand_link', models.CharField(max_length=50, verbose_name='사이트 주소')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('main_category_name', models.CharField(max_length=50, verbose_name='메인 카테고리명')),
                ('main_category_number', models.IntegerField(verbose_name='메인 카테고리 번호')),
                ('sub_category_name', models.CharField(max_length=50, verbose_name='서브 카테고리명')),
                ('sub_category_number', models.IntegerField(verbose_name='서브 카테고리 번호')),
                ('category_link', models.CharField(max_length=50, verbose_name='카테고리 링크')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('post_type', models.CharField(choices=[('REVIEW', '후기(review)'), ('Q&A', '문의(Q&A)')], default='REVIEW', max_length=20, verbose_name='종류')),
                ('post_status', models.CharField(choices=[('NOMAL', '일반'), ('UNANSWERED', '답변 예정'), ('DONE', '답변 완료')], default='NOMAL', max_length=20, verbose_name='상태')),
                ('image', models.ImageField(blank=True, null=True, upload_to='review_images/', verbose_name='이미지')),
                ('content', models.TextField(verbose_name='내용')),
                ('rating', models.IntegerField(blank=True, null=True, verbose_name='평점')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('like', models.ManyToManyField(blank=True, related_name='like_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_number', models.IntegerField(verbose_name='상품번호')),
                ('product_name', models.CharField(max_length=50, verbose_name='상품명')),
                ('product_image', models.CharField(max_length=100, verbose_name='이미지')),
                ('original_price', models.IntegerField(blank=True, null=True, verbose_name='정상가')),
                ('discount_price', models.IntegerField(blank=True, null=True, verbose_name='할인가')),
                ('review_count', models.IntegerField(blank=True, null=True, verbose_name='리뷰')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply', models.TextField(verbose_name='댓글')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('post', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='products.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategoryRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.category')),
                ('products', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(through='products.ProductCategoryRelation', to='products.category'),
        ),
        migrations.AddField(
            model_name='post',
            name='product',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.product'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
