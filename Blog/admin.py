from django.contrib import admin
from Blog.models import Blog, Comment, Likes, Category, Query

# Register your models here.
admin.site.register(Blog),
admin.site.register(Comment),
admin.site.register(Likes),
admin.site.register(Category),
admin.site.register(Query)
