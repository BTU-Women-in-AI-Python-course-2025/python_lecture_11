from django.contrib import admin
from blog.models import BlogPost, BlogPostImage, Author, BannerImage

admin.site.register(BlogPost)
admin.site.register(BlogPostImage)
admin.site.register(Author)
admin.site.register(BannerImage)
