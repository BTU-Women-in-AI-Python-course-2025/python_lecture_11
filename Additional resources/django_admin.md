# Django Admin: Registering Models

## Introduction

Django's admin interface is one of its most powerful features, providing a ready-to-use UI for managing your application's data. 
To make your models accessible through the admin interface, you need to register them.

## Registering Models with Django Admin

### Basic Registration

To make a model accessible in the admin interface, you need to:

1. Import the model
2. Register it using `admin.site.register()`

```python
from django.contrib import admin
from .models import YourModel

admin.site.register(YourModel)
```

### Customizing ModelAdmin

You can customize how your model appears in the admin interface by creating a ModelAdmin class:

```python
from django.contrib import admin
from .models import YourModel

class YourModelAdmin(admin.ModelAdmin):
    list_display = ('field1', 'field2', 'field3')  # Fields to display in list view
    list_filter = ('field1', 'field2')             # Fields to filter by
    search_fields = ('field1', 'field2')           # Fields to search in
    ordering = ('-field1',)                        # Default ordering

admin.site.register(YourModel, YourModelAdmin)
```

### Common ModelAdmin Options

| Option | Description | Example |
|--------|-------------|---------|
| `list_display` | Fields to display in the list view | `('name', 'email', 'created_at')` |
| `list_filter` | Fields to enable filtering by | `('is_active', 'category')` |
| `search_fields` | Fields to enable search functionality | `('title', 'description')` |
| `ordering` | Default ordering of records | `('-created_at',)` |
| `readonly_fields` | Fields that are displayed but not editable | `('created_at', 'updated_at')` |
| `list_per_page` | Number of items per page | `50` |
| `date_hierarchy` | Enable date-based navigation | `'created_at'` |
| `fields` | Control which fields are displayed and their order in the detail view | `('title', 'content', 'author')` |
| `exclude` | Fields to exclude from the form | `('secret_field',)` |

### Inline Models

For related models, you can use inlines to edit them on the parent model's page:

```python
class RelatedModelInline(admin.TabularInline):  # or admin.StackedInline
    model = RelatedModel
    extra = 1  # Number of empty forms to display

class YourModelAdmin(admin.ModelAdmin):
    inlines = [RelatedModelInline]
```

### Decorator Syntax (Alternative Registration)

You can also use the `@admin.register` decorator:

```python
from django.contrib import admin
from .models import YourModel

@admin.register(YourModel)
class YourModelAdmin(admin.ModelAdmin):
    list_display = ('field1', 'field2')
    # other configurations...
```

## Best Practices

1. Always create custom ModelAdmin classes for important models
2. Use `prepopulated_fields` for slug fields based on other fields
3. Consider user permissions when designing admin interfaces
4. Override `save_model()` for custom save behavior
5. Use `get_queryset()` to control which objects are visible

## Example: Complete ModelAdmin Configuration

```python
from django.contrib import admin
from .models import Article, Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')
    search_fields = ('name', 'email')
    
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_published')
    list_filter = ('is_published', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'published_date'
    ordering = ('-published_date',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(is_published=True)

admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
```
