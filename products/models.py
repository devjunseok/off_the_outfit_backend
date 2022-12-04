from django.db import models
from users.models import User


class Brand(models.Model):
    brand_name_kr = models.CharField('브랜드명_국문', max_length=50)
    brand_name_en = models.CharField('브랜드명_영문', max_length=50)
    brand_link = models.CharField('사이트 주소', max_length=50)
    
    def __str__(self):
        return str(self.brand_name_kr)


class Product(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    product_number = models.IntegerField('상품번호')
    product_name = models.CharField('상품명', max_length=50)
    product_image = models.CharField('이미지', max_length=100)
    original_price = models.IntegerField('정상가', null=True, blank=True)
    discount_price = models.IntegerField('할인가', null=True, blank=True)
    review_count = models.IntegerField('리뷰', null=True, blank=True)
    category = models.ManyToManyField("Category", through="ProductCategoryRelation", through_fields=("products", "category"))
    
    def __str__(self):
        return str(self.product_name)
  
    
class Category(models.Model):
    main_category_name = models.CharField('메인 카테고리명', max_length=50)
    main_category_number = models.IntegerField('메인 카테고리 번호')
    sub_category_name = models.CharField('서브 카테고리명', max_length=50)
    sub_category_number = models.IntegerField('서브 카테고리 번호')
    category_link = models.CharField('카테고리 링크', max_length=50)
        
    def __str__(self):
        return str(self.sub_category_name)


class ProductCategoryRelation(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    POST_TYPE = (
        ('REVIEW', '후기(review)'),
        ('Q&A', '문의(Q&A)'),
    )
    
    POST_STATUS = (
        ('NOMAL', '일반'),
        ('UNANSWERED', '답변 예정'),
        ('DONE', '답변 완료'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, related_name='products')
    post_type = models.CharField('종류', choices=POST_TYPE, max_length=20, default=POST_TYPE[0][0])
    post_status = models.CharField('상태', choices=POST_STATUS, max_length=20, default=POST_STATUS[0][0])
    image = models.ImageField('이미지', blank=True, upload_to="review_images/", null=True)
    content = models.TextField('내용')
    rating = models.IntegerField('평점', null=True, blank=True)
    like = models.ManyToManyField(User, related_name='like_reviews', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.content)
    
class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, related_name="posts")
    reply = models.TextField('댓글')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.reply)