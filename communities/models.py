from django.db import models
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from users.models import User
from products.models import Product

# Create your models here.
class TaggedFeed(TaggedItemBase): # 태그추가 부분
    content_object = models.ForeignKey('Feed', on_delete=models.CASCADE)


class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(blank=True, upload_to="feed_images/", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, related_name='like_posts', blank=True)
    unlike = models.ManyToManyField(User, related_name='unlike_posts', blank=True)
    report_point = models.PositiveIntegerField("신고 포인트", default=0)
    tags = TaggableManager(through=TaggedFeed, blank=True)
    
    def __str__(self):
        return str(self.content)
    

class Comment(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, blank=True, related_name="feeds")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_like = models.ManyToManyField(User, related_name='like_comments', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ReComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recomment = models.TextField(blank=True ,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    recomment_like = models.ManyToManyField(User, related_name='like_recomments', blank=True)
    


class FeedProductRelation(models.Model):
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    