from django.contrib import admin
from blog.models import BlogPost, BlogPostImage, BannerImage
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin


@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    raw_id_fields = ('blog_post',)


# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'age')


class MembershipInline(admin.TabularInline):
    model = BlogPost.authors.through
    extra = 1


class BlogPostImageInline(SortableInlineAdminMixin, admin.StackedInline):
    model = BlogPostImage
    extra = 7
    max_num = 5
    ordering = ['order']


class BlogPostAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [MembershipInline, BlogPostImageInline]
    list_display = ('title', 'active', 'deleted')
    list_filter = ('active', 'deleted')
    search_fields = ('title',)
    # ordering = ('order',)
    date_hierarchy = 'create_date'
    # list_per_page = 1
    # fields = ('title', 'active', 'deleted', 'order')
    # exclude = ('title',)
    # filter_vertical = ('authors',)
    filter_horizontal = ('authors',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(active=True)

admin.site.register(BlogPost, BlogPostAdmin)
