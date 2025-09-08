from django.contrib import admin
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from nested_admin.nested import NestedTabularInline, NestedModelAdmin

from blog.models import BlogPost, BlogPostImage, BannerImage, BlogPostImageDescription
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin

from blog.resources import BlogPostResource


@admin.register(BannerImage)
class BannerImageAdmin(admin.ModelAdmin):
    raw_id_fields = ('blog_post',)


# @admin.register(Author)
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('full_name', 'age')


class MembershipInline(admin.TabularInline):
    model = BlogPost.authors.through
    extra = 1

#
# class BlogPostImageInline(SortableInlineAdminMixin, admin.StackedInline):
#     model = BlogPostImage
#     extra = 7
#     max_num = 5
#     ordering = ['order']

class BlogPostImageDescriptionInline(NestedTabularInline):
    model = BlogPostImageDescription
    extra = 1

class BlogPostImageInline(NestedTabularInline):
    model = BlogPostImage
    inlines = [BlogPostImageDescriptionInline]
    extra = 1


# class BlogPostAdmin(SortableAdminMixin, NestedModelAdmin):
#     # inlines = [MembershipInline, BlogPostImageInline]
#     resource_class = BlogPostResource
#     inlines = [BlogPostImageInline]
#     list_display = ('title', 'active', 'deleted')
#     list_filter = ('active', 'deleted')
#     search_fields = ('title',)
#     # ordering = ('order',)
#     date_hierarchy = 'create_date'
#     # list_per_page = 1
#     # fields = ('title', 'active', 'deleted', 'order')
#     # exclude = ('title',)
#     # filter_vertical = ('authors',)
#     filter_horizontal = ('authors',)
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         if request.user.is_superuser:
#             return qs
#         return qs.filter(active=True)


class BlogPostAdmin(ImportExportModelAdmin):
    # inlines = [MembershipInline, BlogPostImageInline]
    resource_class = BlogPostResource
    list_display = ('title', 'active', 'deleted')
    actions = ['export_selected']

    def export_selected(self, request, queryset):
        """Custom export action"""
        resource = BlogPostResource()
        dataset = resource.export(queryset)
        response = HttpResponse(
            dataset.export('xlsx'),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="books.xlsx"'
        return response


admin.site.register(BlogPost, BlogPostAdmin)
