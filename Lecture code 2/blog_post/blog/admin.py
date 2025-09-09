from django.contrib import admin
from blog.models import BlogPost, BlogPostImage, Author, BlogPostCover

admin.site.register(BlogPostImage)
admin.site.register(Author)
admin.site.register(BlogPostCover)


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'authors')
    search_fields = ('title',)
    ordering = ('-title',)
    date_hierarchy = 'created_at'
    filter_horizontal = ('authors',)
    prepopulated_fields = {'slug': ('title',)}
    # readonly_fields = ('title',)
    # list_per_page = 2
    # fields = ('title', 'is_active', 'text')
    # exclude = ('text',)
    # filter_vertical = ('authors',)
    # fieldsets = (
    #     ("Basic Information", {
    #         "fields": ("title", "text", "website")
    #     }),
    #     ("Many to Many", {
    #         "fields": ("authors",)
    #     })
    # )


admin.site.register(BlogPost, BlogPostAdmin)
