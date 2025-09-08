from import_export import resources
from blog.models import BlogPost


class BlogPostResource(resources.ModelResource):
    class Meta:
        model = BlogPost
        # Optional: Control which fields are included
        fields = ('id', 'title', 'text', 'create_date')
