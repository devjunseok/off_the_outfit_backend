from django.contrib import admin
from communities.models import Feed, Comment,ReComment

# Register your models here.
admin.site.register(Feed)
admin.site.register(Comment)
admin.site.register(ReComment)

