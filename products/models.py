from django.db import models

# Create your models here.

class Brand(models.Model):
    brand_name_kr = models.CharField('브랜드명_국문', max_length=50)
    brand_name_en = models.CharField('브랜드명_영문', max_length=50)
    brand_link = models.CharField('사이트 주소', max_length=50)
    
    def __str__(self):
        return str(self.brand_name_kr)


class Products(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_number = models.IntegerField('상품번호')
    product_name = models.CharField('상품명', max_length=50)
    product_image = models.CharField('이미지', max_length=100)
    original_price = models.IntegerField('정상가', null=True, blank=True)
    discount_price = models.IntegerField('할인가', null=True, blank=True)
    review_count = models.IntegerField('리뷰', null=True, blank=True)
    category = models.ManyToManyField("Category", through="ProductCategoryRelation", through_fields=("products", "category"))
    
    def __str__(self):
        return str(self.products_name)
  
    
class Category(models.Model):
    main_category_name = models.CharField('메인 카테고리명', max_length=50)
    main_category_number = models.IntegerField('메인 카테고리 번호')
    sub_category_name = models.CharField('서브 카테고리명', max_length=50)
    sub_category_number = models.IntegerField('서브 카테고리 번호')
    category_link = models.CharField('카테고리 링크', max_length=50)
        
    def __str__(self):
        return str(self.sub_category_name)


class ProductCategoryRelation(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    
