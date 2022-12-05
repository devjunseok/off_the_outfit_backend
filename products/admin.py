from django.contrib import admin
from products.models import *

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductCategoryRelation)
admin.site.register(Post)
admin.site.register(Reply)