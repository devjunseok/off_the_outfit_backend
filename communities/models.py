from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from users.models import User
from products.models import Product

# Create your models here.
class TaggedFeed(TaggedItemBase): # 태그추가 부분
    content_object = models.ForeignKey('Feed', on_delete=models.CASCADE)


class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feeds')
    content = models.TextField('게시글 본문')
    image = models.ImageField('게시글 사진', blank=True, upload_to="feed_images/", null=True)
    created_at = models.DateTimeField('게시글 생성 일자',auto_now_add=True)
    updated_at = models.DateTimeField('게시글 수정 일자', auto_now=True)
    like = models.ManyToManyField(User, related_name='like_posts', blank=True)
    unlike = models.ManyToManyField(User, related_name='unlike_posts', blank=True)
    report_point = models.PositiveIntegerField("신고 포인트", default=0)
    tags = TaggableManager(through=TaggedFeed, blank=True)
    
    def __str__(self):
        return str(self.content)
    

class Comment(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, blank=True, related_name="feeds")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField('댓글 본문')
    comment_like = models.ManyToManyField(User, related_name='like_comments', blank=True)
    created_at = models.DateTimeField('댓글 생성 일자', auto_now_add=True)
    updated_at = models.DateTimeField('댓글 수정 일자', auto_now=True)


class ReComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recomment = models.TextField('대댓글 본문', blank=True ,null=True)
    created_at = models.DateTimeField('대댓글 생성 일자', auto_now_add=True)
    recomment_like = models.ManyToManyField(User, related_name='like_recomments', blank=True)
    

class FeedProductRelation(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    

class ReportFeed(models.Model): # 신고 내용 저장 테이블
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, blank=True, related_name="reports")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report = models.TextField('신고내용')
    created_at = models.DateTimeField('신고일자', auto_now_add=True)
    

class SearchWord(models.Model): # 검색어 저장 테이블
    word = models.CharField('검색어', max_length=30)
    created_at = models.DateTimeField('검색일자', auto_now_add=True)