from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from django.http import HttpResponse
from import_export.admin import ImportExportModelAdmin
from nested_admin.nested import NestedTabularInline, NestedModelAdmin

from blog.models import BlogPost, BlogPostImage, Author, BlogPostImageDescription
from blog.resources import BlogPostResource, AuthorResource


@admin.register(Author)
class AuthorAdmin(ImportExportModelAdmin):
    resource_class = AuthorResource
    actions = ['export_selected']
    list_display = ('full_name', 'age')

    def export_selected(self, request, queryset):
        """Custom export action"""
        resource = AuthorResource()
        dataset = resource.export(queryset)
        response = HttpResponse(
            dataset.export('xlsx'),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="books.xlsx"'
        return response


# class BlogPostImageInline(SortableInlineAdminMixin, admin.TabularInline):
#     model = BlogPostImage
#     extra = 1


# class BlogPostAdmin(SortableAdminMixin, admin.ModelAdmin):
#     inlines = [BlogPostImageInline]
#     list_display = ('title', 'is_active', 'created_at')
#     list_filter = ('is_active', 'authors')
#     search_fields = ('title',)
#     date_hierarchy = 'created_at'
#     filter_horizontal = ('authors',)
#     prepopulated_fields = {'slug': ('title',)}
#     # list_per_page = 2
#     # fields = ('title', 'is_active', 'text')
#     # exclude = ('text',)
#     # filter_vertical = ('authors',)
#     # fieldsets = (
#     #     ("Basic Information", {
#     #         "fields": ("title", "text", "website")
#     #     }),
#     #     ("Many to Many", {
#     #         "fields": ("authors",)
#     #     })
#     # )


class BlogPostImageDescriptionInline(NestedTabularInline):
    model = BlogPostImageDescription
    extra = 1

class BlogPostImageInline(NestedTabularInline):
    model = BlogPostImage
    inlines = [BlogPostImageDescriptionInline]
    extra = 1

class BlogPostAdmin(ImportExportModelAdmin, NestedModelAdmin):
    resource_class = BlogPostResource
    inlines = [BlogPostImageInline]
    list_display = ('title', 'is_active', 'created_at')

admin.site.register(BlogPost, BlogPostAdmin)
