from django.db import models

# Create your models here.

class Brand(models.Model):
    brand_name_kr = models.CharField('브랜드명_국문', max_length=50)
    brand_name_en = models.CharField('브랜드명_영문', max_length=50)
    brand_link = models.CharField('사이트 주소', max_length=50)


class Products(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    products_name = models.CharField('상품명', max_length=50)
    original_price = models.IntegerField('정상가')
    discount_price = models.IntegerField('할인가')
    discount_rate = models.DecimalField('할인율', max_digits=3, decimal_places=2)
    review_count = models.IntegerField('리뷰')
    category = models.ManyToManyField("Category", blank=True, through="ProductCategoryRelation")
    
    class Meta:
        db_table = 'Products'
  
    
class Category(models.Model):
    main_category_name = models.CharField('메인 카테고리명', max_length=50)
    main_category_number = models.IntegerField('메인 카테고리 번호')
    sub_category_name = models.CharField('서브 카테고리명', max_length=50)
    sub_category_number = models.IntegerField('서브 카테고리 번호')
    
    class Meta:
        db_table = 'Category'


class ProductCategoryRelation(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'ProductCategoryRelation'
    
