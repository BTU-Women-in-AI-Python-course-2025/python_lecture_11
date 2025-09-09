from import_export import resources, fields
from blog.models import BlogPost, Author


class BlogPostResource(resources.ModelResource):
    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'text', 'created_at', 'is_active')

class AuthorResource(resources.ModelResource):
    full_name = fields.Field(column_name='full_name', attribute='full_name')

    class Meta:
        model = Author
        fields = ('id', 'full_name')

    def dehydrate_full_name(self, author):
        return f"{author.first_name} {author.last_name}"
